# Online-Outpass-System
## Features
- Student login → raise outpass (reason, from/to datetime)
- Warden portal → approve/reject (forwards to incharge)
- Hostel Incharge portal → final approve/reject
- Student can view status and **download/print approved pass**
- Seed demo users (created on first run)
  - Student: `srimathi2410307@ssn.edu` / `1234`

## Tech Stack
- Python Flask,Bootstrap (CDN)

## Project Structure
```
online-outpass-system/
├─ app.py
├─ templates/
│  ├─ login.html
│  ├─ dashboard.html
│  ├─ apply_outpass.html
│  ├─ check_status.html
│  └─ download_approved_outpass
```

##  Demo Flow
1. Login as Student → submit a request (reason + from/to).
2. In Dashboard there will be three options(Apply for outpass,Check status,Download approved pass)
3. In Apply for outpass all the required fields must be filled.A confirmation mail will be sent to the recipient
4. In check status the student must enter the application number and check their outpass request status
5. Once it is approved the outpass can be downloaded by the student

#  Repository Link
https://srimathi109.github.io/Online-Outpass-System/
