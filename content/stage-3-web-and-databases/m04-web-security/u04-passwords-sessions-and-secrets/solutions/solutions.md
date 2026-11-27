# Passwords, sessions, and secrets

## `register`

Each registration gets its own salt. scrypt uses O(n × r × p) work and O(n × r) main memory for this profile. Encoding also costs O(b) for b password bytes.

## `verify`

Bounded profiles keep storage mistakes from selecting huge costs. Valid verification uses O(n × r × p) work and O(n × r) main memory, plus O(b) encoding time and space.

## `login`

A successful login can replace an older record with a stronger one without storing plaintext. A record that is already as strong or stronger stays as it is. Time is one verification plus at most one registration, with O(1) work of its own for the dictionary lookup and write. Peak extra space is the higher KDF memory cost.

## Next practice

Compare a valid and invalid login in the toy app. Add a case for a stale profile and one for an expired reset.
