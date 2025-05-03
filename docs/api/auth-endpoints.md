# Authentication API Documentation
**Base URL:** `/api/auth/`

---

## **Endpoints**

---

### **1. Register User**
**URL:** `/register/`
**Method:** `POST`
Registers a new user and sends an OTP via email for verification.

#### Request Body (JSON):
```json
{
  "username": "kerciu",
  "email": "kacpergorski@example.com",
  "first_name": "Kacper",
  "last_name": "Gorski",
  "password": "securepassword123",
  "re_password": "securepassword123"
}
```

#### Responses:
| Status Code | Description | Example Response |
|-------------|-------------|------------------|
| `201 Created` | User created successfully | `{ "data": {"username": "kerciu", "email": "kacpergorski@example.com", "first_name": "Kacper", "last_name": "Gorski", "password": "securepassword123", "re_password": "securepassword123"}, "message": "Check your email for verification passcode" }` |
| `400 Bad Request` | Validation error (e.g., passwords mismatch, email exists) | `{ "username": ["This field is required."], "email": ["Enter a valid email address."], "password": ["Ensure this field has at least 6 characters."], "re_password": ["Ensure this field has at least 6 characters."] }` |

---

### **2. Verify User Email**
**URL:** `/verify-user/`
**Method:** `POST`
Validates the OTP sent to the user's email.

#### Request Body (JSON):
```json
{ "otp": "213769" }
```

#### Responses:
| Status Code | Description | Example Response |
|-------------|-------------|------------------|
| `200 OK` | Account verified | `{ "message": "Account verified successfully" }` |
| `208 Already Reported` | Account already verified | `{'message': 'Account is already verified'}` |
| `404 Not Found` | Invalid OTP | `{ "message": "Passcode not provided" }` |

---

### **3. Resend Verification Email**
**URL:** `/resend-email/`
**Method:** `POST`
Resends a new OTP to the user's email.

#### Request Body (JSON):
```json
{ "email": "kacpergorski@example.com" }
```

#### Responses:
| Status Code | Description | Example Response |
|-------------|-------------|------------------|
| `200 OK` | New OTP sent | `{ "message": "New verification code has been sent" }` |
| `404 Not Found` | Email not registered | `{ "message": "User with this email does not exist!" }` |

---

### **4. Login User**
**URL:** `/login/`
**Method:** `POST`
Authenticates a user and returns JWT tokens.

#### Request Body (JSON):
```json
{
  "email": "kacpergorski@example.com",
  "password": "securepassword123"
}
```

#### Responses:
| Status Code | Description | Example Response |
|-------------|-------------|------------------|
| `200 OK` | Login success | `{ "email": "...", "full_name": "...", "access": "...", "refresh": "..." }` |
| `400 Bad Request` | Invalid credentials | `{ "error": "Invalid credentials" }` |
| `401 Unauthorized` | Email not verified | `{ "error": "Email is not verified" }` |

---

### **5. Refresh Access Token**
**URL:** `/token/refresh/`
**Method:** `POST`
Generates a new access token using a valid refresh token.

#### Request Body (JSON):
```json
{ "refresh": "2imu3wd823thisisrefreshtoken324ur238r" }
```

#### Responses:
| Status Code | Description | Example Response |
|-------------|-------------|------------------|
| `200 OK` | New access token | `{ "access": "2137udwiefkuhn2uerfydnew" }` |
| `401 Unauthorized` | Invalid/expired refresh token | `{ "detail": "Token is invalid or expired" }` |

---

### **6. Password Reset Request**
**URL:** `/password-reset/`
**Method:** `POST`
Sends a password reset link to the user's email.

#### Request Body (JSON):
```json
{ "email": "kacpergorski@example.com" }
```

#### Responses:
| Status Code | Description | Example Response |
|-------------|-------------|------------------|
| `200 OK` | Reset link sent (if email exists) | `{ "message": "If this email exists, a reset link has been sent" }` |

---

### **7. Password Reset Confirm**
**URL:** `/password-reset-confirm/<uid>/<token>/`
**Method:** `GET`
Validates the password reset token.

#### Responses:
| Status Code | Description | Example Response |
|-------------|-------------|------------------|
| `200 OK` | Valid token | `{ "success": true, "message": "Credentials are valid", "uid": uid, "token": token, }` |
| `401 Unauthorized` | Invalid/expired token | `{ "success": false, "message": "Token is invalid or expired" }` |

---

### **8. Set New Password**
**URL:** `/set-new-password/`
**Method:** `PATCH`
Updates the user's password after token validation.

#### Request Body (JSON):
```json
{
  "password": "newpassword123",
  "confirm_password": "newpassword123",
  "uid": "<encoded_uid>",
  "token": "<reset_token>"
}
```

#### Responses:
| Status Code | Description | Example Response |
|-------------|-------------|------------------|
| `200 OK` | Password updated | `{ "message": "Password reset successfully" }` |
| `400 Bad Request` | Passwords mismatch | `{ "error": "Passwords do not match" }` |
| `401 Unauthorized` | Invalid token | `{ "error": "Reset link is invalid" }` |

---

### **9. Logout User**
**URL:** `/logout/`
**Method:** `POST`
Invalidates the user's refresh token.

#### Request Body (JSON):
```json
{ "refresh_token": "2983ryj287iryn2n38tokeno32ir328" }
```

#### Responses:
| Status Code | Description |
|-------------|-------------|
| `205 Reset Content` | Logout success |
| `400 Bad Request` | Invalid token |

---

### **10. Google OAuth2 Login**
**URL:** `/google-auth/`
**Method:** `POST`
Authenticates a user using Google OAuth2.

#### Request Body (JSON):
```json
{ "access_token": "<google_access_token>" }
```

#### Responses:
| Status Code | Description | Example Response |
|-------------|-------------|------------------|
| `200 OK` | Login success | `{ "email": "...", "full_name": "...", "access": "...", "refresh": "..." }` |
| `403 Unauthorized` | Provider conflict | `{ "detail": "Please continue your login using <different auth method>" }` |
| `401 Unauthorized` | Invalid token | `{ "error": "Token is invalid" }` |

---

### **11. GitHub OAuth2 Login**
**URL:** `/github-auth/`
**Method:** `POST`
Authenticates a user using GitHub OAuth2.

#### Request Body (JSON):
```json
{ "code": "<github_authorization_code>" }
```

#### Responses:
| Status Code | Description | Example Response |
|-------------|-------------|------------------|
| `200 OK` | Login success | `{ "email": "...", "full_name": "...", "access": "...", "refresh": "..." }` |
| `403 Unauthorized` | Provider conflict | `{ "detail": "Please continue your login using <different auth method>" }` |
| `400 Bad Request` | Invalid code | `{ "error": "Invalid code" }` |
