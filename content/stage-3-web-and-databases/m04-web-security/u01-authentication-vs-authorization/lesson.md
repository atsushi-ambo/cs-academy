# Authentication vs authorization

## Why

A staff login should open only the reports that person may use.

## Request path

```text
session key -> user lookup -> policy(user, action, report) -> decision
```

The server looks up the user and checks the action on the requested report.

## Example

A north admin may read a north report owned by someone else.
The same admin may edit only their own reports. A south report stays out of scope.

## Common mistakes

- Hiding a link leaves the server route reachable.
- A random identifier can still appear in a shared link.
- A client-supplied role is outside the server's trusted identity record.

## At work

Test a valid session with the wrong owner or organization on every sensitive route.
Check list results as well as single-report requests.

## Summary

Authenticate the actor, find the requested object, and authorize the action before returning data.

## Model answer

The session tells the server who made the request. The report policy checks that identity against the requested report. If no rule allows the action, the server denies it.
