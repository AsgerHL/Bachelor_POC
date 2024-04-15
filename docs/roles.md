# Role, Special roles, and Alias

There are different roles and alias types in the OS2datascanner system.
Each role or alias has different permissions and responsibilities
through both the Admin- and Report module.

All of the database objects that control this behaviour are managed through the
administration module and are automatically reflected (in a read-only form) to
the report module.

These objects are usually created and updated by automatically importing them
from external directory systems, but you can also create your own from within
OS2datascanner -- or add some extras on top of an imported directory.

## Roles

OS2datascanner uses a simplified form of [Role-Based Access Control](https://en.wikipedia.org/wiki/Role-based_access_control) to determine what functions a user should have
access to.

Roles are assigned through the `Position` object. Each `Position` specifies a
type of role: employee, manager or data protection officer. It relates an
`Account` object with that role to an `OrganizationalUnit`, which is a
component of the organizational hierarchy.
This means a user can have different roles in different contexts: someone may
be a manager of one department, a DPO of a second, and a normal employee of a
third.

Roles are meant to provide a more structured organization by granting some roles
access to different features in the system.

### Employee

The Employee role specifies that an account should be scanned if the related
organizational unit is specified in an account-based scannerjob. For example,
an O365 mailscanner specifying three organizational units will scan all
accounts related to those units through Position-objects with the "employee"
role.

#### Assigning an Employee

When importing an organizational structure from an external directory system,
employee roles are automatically assigned to all users.

If an employee is to be assigned manually, it can be done through the Django
administration system, available through the `Administration` tab in the admin
module.
From here, select `Positions` under `Organizations`.

When adding an employee, you must choose an account to receive the role and then
the organizational unit they should be assigned to. Lastly, select `employee` from the
role dropdown.

*Note: Only superusers can assign the employee role manually. See the "Special
Roles" section further down for more information.*

### Manager

The manager role gives access to a page called "Leader overview" in the report
module.
On the leader overview page, a manager is presented with a list of all employees
associated with the relevant organizational unit.

The manager can see how the individual employee fares in handling matches
they have received in the past year.

The leader overview page lists each employee with a "status".
An employee can have 1 of 3 statuses:

* `Completed`: All matches the employee received have been handled.
* `Accepted`: 75% of matches the employee received the past 3 weeks have been
handled.
* `Not Accepted`: Less than 75% of matches the employee has received the past
3 weeks have been handled.

When selecting an employee from the list, the leader overview page offers more
information about matches handled and received during the past 3 weeks. (This
shows the same information as the employee's own statistics page.)

#### Assigning a Manager

To assign a manager, choose an account to receive the role by clicking the "+"
under "Managers" on the organizational structure page. The organizational
structure page is found under the `Organization` tab in the admin module.

### Data Protection Officer (DPO)

The DPO role gives access to a page called "DPO Overview" in the report module.
The DPO Overview page displays statistics regarding matches associated with the
relevant organizational unit.
For example:

- The percentage of matches found in different sources.

- How many new matches have been found in a given month.

- The percentage of matches handled in the organizational unit.

#### Assigning a DPO

To assign a DPO, choose an account to receive the role by clicking the "+"
under "DPOs" on the organizational structure page. The organizational structure
page is found under the `Organization` tab in the admin module.

## Aliases

The `Alias` object associates a piece of typed metadata with a user. These
assocations are used to establish relationships between users and the matches
found when a scan is run.

An `Alias` object consists of a relation to an `Account`, an alias type, and a
value.

The alias type specifies what type of identifier the alias contains.

There are 4 identifiers in the system:

* `SID`
* `E-mail`
* `Remediator`
* `Generic`

The value typically contains what is specified in the alias type.
For instance, when creating an alias with the type e-mail, the value would
be an e-mail address.

The following points will go into further detail about the alias types
and how to assign them to an account.

*Note: Only superusers can assign an alias.*

### Security Identifier (SID)

An SID is a unique identifier for security entities (users or groups) in a
Windows domain.
When a user signs in, an access token containing the SID and rights of the user
is created. The token provides security context for the user's actions
performed during that session.

A typical SID could look like this:

`S-1-5-21-1004336348-1177238915-682003330-512`

(For more information about the structure and significance of SIDs, consult
[Microsoft's documentation](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-identifiers).)

#### Why SID?

When creating a file in a shared network drive, the system needs a way
to remember who created it. This is done by saving the SID of the creator
of the file. OS2datascanner can then read this information and use it to assign
the creator of a file the responsibility for resolving its matches.

For OS2datascanner to make the right associations, an account must be given
an alias with the SID type and a value matching the user's SID.

This is relevant when using the file scanner.

#### Assigning an SID Alias

SID aliases are automatically created when importing users with Microsoft Graph
(Azure AD/Entra ID). In other cases, it is presently necessary to retrieve this
information manually from the directory system.

To assign the SID alias, first access the Django administration system,
available through the `Administration` tab in the admin module.
From here, select `Aliases` under `organizations` and click `Add Alias`.
Choose the related account and then the SID alias type from the
"Alias type:" dropdown.

Input the SID of the user in the alias's `Value` field.

### E-mail

The e-mail alias type is used for scanner jobs where the owner or creator of the
objects containing matches can be identified by an e-mail address.

For example, scanner jobs using `Office365`-scans will provide an e-mail address
in the `owner`-field of the document reports.

#### Assigning an E-mail Alias

To assign the e-mail alias, first access the Django administration system,
available through the `Administration` tab in the admin module.
From here, select `Aliases` under `organizations` and click `Add Alias`.
Choose the related account and then the e-mail alias type from the
"Alias type:" dropdown.

If there is uncertainty about what e-mail address should be used as the alias value,
look at the document reports for that scan.
Each document report contains an `owner`-field with the value of the owner/creator.
(Document reports can be displayed through the Django administration system.)

Input the e-mail address of the user in the alias's `Value` field.

### Remediator

When a match cannot be linked to any other account, it is assigned to the
relevant remediator.

An example of this could be files in a shared drive created by a former coworker.
Their SID is still recorded as the owner of the file, but the directory system
no longer includes them, so the owner of the files cannot be linked to a user.

#### Assigning a Remediator Alias

To assign the remediator alias, first access the Django administration system,
available through the `Administration` tab in the admin module.
From here, select `Aliases` under `organizations` and click `Add Alias`.
Choose the related account and then the remediator alias type from the
"Alias type:" dropdown.

The value of a remediator *must* be a number.

If a remediator should receive matches from a specific scanner job, input the
`primary key(PK)` of that scanner job in the alias's `Value`-field.
The `PK` of the scanner job can be found in the `Scanner job pk`-field of the
document reports.
(Document reports can be displayed through the Django administration system.)

A remediator can also be assigned matches from all scanner jobs by inputting
`0` as the alias's value.

### Generic

When no other types of aliases are appropriate, the 'generic' type is an unspecific fallback,
which can be assigned any value.

The generic alias type can be used for scans like `Webscanner`.
When running a webscan, the owner of matches is set to the root URL of the scanned website.
The generic alias type is then used to assign an account the owner of those matches.

#### Assigning a Generic Alias

To assign the generic alias, first access the Django administration system,
available through the `Administration` tab in the admin module.
From here, select `Aliases` under `organizations` and click `Add Alias`.
Choose the related account and then the generic alias type from the
"Alias type:" dropdown.

for scans like `webscanner`, input the root URL in the alias's `Value` field.
If there is uncertainty about what should be used as the alias value,
look at the document reports for that scan.
Each document report contains an `owner`-field with the value of the owner/creator.
Document reports are found on the django-admin page in the report module.
Input the value found in the document report into the alias's `value` field.

## Special Roles

OS2datascanner contains two modules: the admin module and the report module.

Special roles are assigned to the `User` objects in the database.

Users within these two modules are not the same, meaning that if a user
is created in the admin module, it won't be in the report module.

When an account is added in the admin module, it is extended to the report module,
where users are then created based on the accounts.

Since the users aren't the same across the system, it is possible for a user
to have privileges in one module but not the other.

### Superuser

The superuser role provides a user access to almost *everything*
across all clients.

Depending on the module, the superuser has access to different features.

Superusers in the admin module are the only users that can validate scans.
Scans that haven't been validated by a superuser will be unable to run
Superusers in the admin module are also the only users with permission
to access the Django administration system page. This means that features like
manually creating  users and assigning roles and aliases can only be done by a
superuser.

In the report module, superusers have access to withheld matches and are
therefore the only users who can distribute them.

When creating a scanner job, a setting called "only notify superadmin"
can be checked, so that all matches found during that scan won't be distributed
and can only be seen by the superusers in the report module.

Superusers have access to all features other roles have, meaning
features accessible to managers and DPOs are also accessible to the superuser.

*Note that since the superuser has extended privileges,
the role should be used very sparingly.*

#### Assigning a Superuser in The Admin Module

To assign a superuser in the admin module, first access the Django
administration system,
available through the `Administration` tab in the admin module.
If it hasn't been done, create a user under `Users` and click `Add user`.

When creating the user, be sure to check the `Superuserstatus` checkbox
for them to have superuser privileges.

#### Assigning a Superuser in The Report Module

To assign a superuser in the report module, first access the Django
administration system,
available through the `Administration` tab in the admin module.
Users in the report module are created from accounts in the admin module.

When creating an account, click `Accounts` under `organizations` and
check the `Superuser_status` checkbox.

(It is possible to assign superuser status directly in the report module, but
this is not recommended. As the admin module is considered to be the
authoritative source of user information, any changes made may be discarded at
any time.)

### Admin

The admin role give users admin permissions on the client they have been assigned to.
In contrast, a superuser role has access to all permissions on all clients.

From the Django administration system an admin can create, edit, and delete
rules, assign
managers and DPOs, or add new organizations.

The admin also has permission to create, run, edit, and delete scanner jobs.

When an admin creates a scanner job, it has to be validated by a
superuser.
If a scanner job hasn't been validated it will be unable to run.

On the report module the admin has access to the Django administration system.

#### Assigning an Admin in The Admin Module

The admin role is assigned on the Django administration system in the admin module.

For an admin to be assigned, a user and a client must exist.
To create a user, access the `Users` tab and click `Add user`.
To create a client, access the `Clients` tab and click `Add client`.
Assigning an admin is done by accessing the `Administrators` tab and clicking
`Add administrator`.
From here, choose a user to receive the role and a client they should be assigned to.

#### Assigning an Admin in The Report Module

The admin role is assigned on the Django administration system in the report
module.

To assign the admin, choose a user under the `Users` tab. From here, check the
`Admin-status` checkbox for that user.
