from os import getpid
import pika

from ...utils.prometheus import prometheus_session
from ..model.core import (Source, SourceManager, ResourceUnavailableError,
        DeserialisationError)
from .utilities import (notify_ready, notify_stopping, prometheus_summary,
        json_event_processor, make_common_argument_parser)

args = None


@prometheus_summary("os2datascanner_pipeline_explorer", "Sources explored")
@json_event_processor
def message_received(channel, method, properties, body):
    print("message_received({0}, {1}, {2}, {3})".format(
            channel, method, properties, body))
    channel.basic_ack(method.delivery_tag)

    try:
        source = Source.from_json_object(body["source"])

        # The configuration dictionary was added fairly late to scan specs, so
        # not all clients will send it. Add an empty one if necessary
        body.setdefault("configuration", {})

        if "progress" in body:
            # If this scan spec is based on a derived source and so contains
            # scan progress information, then take it out; the rest of the
            # pipeline won't look for it here
            progress = body["progress"]
            del body["progress"]
        else:
            progress = dict(rule=body["rule"], matches=[])

        with SourceManager() as sm:
            for handle in source.handles(sm):
                print(handle)
                yield (args.conversions, {
                    "scan_spec": body,
                    "handle": handle.to_json_object(),
                    "progress": progress
                })
    except ResourceUnavailableError as ex:
        yield (args.problems, {
            "where": body["source"],
            "problem": "unavailable",
            "extra": [str(arg) for arg in ex.args]
        })
    except DeserialisationError as ex:
        yield (args.problems, {
            "where": body["source"],
            "problem": "malformed",
            "extra": [str(arg) for arg in ex.args]
        })
    except KeyError as ex:
        yield (args.problems, {
            "where": body,
            "problem": "malformed",
            "extra": [str(arg) for arg in ex.args]
        })


def main():
    parser = make_common_argument_parser()
    parser.description = "Consume sources and generate conversions."

    inputs = parser.add_argument_group("inputs")
    inputs.add_argument(
            "--sources",
            metavar="NAME",
            help="the name of the AMQP queue from which scan specifications"
                    + " should be read",
            default="os2ds_scan_specs")

    outputs = parser.add_argument_group("outputs")
    outputs.add_argument(
            "--conversions",
            metavar="NAME",
            help="the name of the AMQP queue to which conversions should be"
                    + " written",
            default="os2ds_conversions")
    outputs.add_argument(
            "--problems",
            metavar="NAME",
            help="the name of the AMQP queue to which problems should be"
                    + " written",
            default="os2ds_problems")

    global args
    args = parser.parse_args()

    parameters = pika.ConnectionParameters(host=args.host, heartbeat=6000)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.queue_declare(args.sources, passive=False,
            durable=True, exclusive=False, auto_delete=False)
    channel.queue_declare(args.conversions, passive=False,
            durable=True, exclusive=False, auto_delete=False)
    channel.queue_declare(args.problems, passive=False,
            durable=True, exclusive=False, auto_delete=False)

    channel.basic_consume(args.sources, message_received)

    with prometheus_session(
            str(getpid()),
            args.prometheus_dir,
            stage_type="explorer"):
        try:
            print("Start")
            notify_ready()
            channel.start_consuming()
        finally:
            print("Stop")
            notify_stopping()
            channel.stop_consuming()
            connection.close()


if __name__ == "__main__":
    main()