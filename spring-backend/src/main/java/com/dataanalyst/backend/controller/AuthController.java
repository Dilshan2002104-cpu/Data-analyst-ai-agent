package com.dataanalyst.backend.controller;

import com.dataanalyst.backend.dto.AuthRequest;
import com.dataanalyst.backend.dto.AuthResponse;
import com.dataanalyst.backend.model.User;
import com.dataanalyst.backend.service.FirebaseService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.Instant;
import java.util.UUID;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private static final Logger logger = LoggerFactory.getLogger(AuthController.class);
    private final FirebaseService firebaseService;

    public AuthController(FirebaseService firebaseService) {
        this.firebaseService = firebaseService;
    }

    @PostMapping("/register")
    public ResponseEntity<AuthResponse> register(@RequestBody AuthRequest request) {
        try {
            logger.info("Registration request for email: {}", request.getEmail());

            // In a real app, you'd use Firebase Authentication
            // For now, we'll create a simple user
            String uid = UUID.randomUUID().toString();

            User user = User.builder()
                    .uid(uid)
                    .email(request.getEmail())
                    .displayName(request.getDisplayName())
                    .createdAt(Instant.now())
                    .lastLoginAt(Instant.now())
                    .build();

            User createdUser = firebaseService.createUser(user);

            AuthResponse response = AuthResponse.builder()
                    .success(true)
                    .message("User registered successfully")
                    .user(createdUser)
                    .token(uid) // In production, generate proper JWT
                    .build();

            return ResponseEntity.ok(response);

        } catch (Exception e) {
            logger.error("Error registering user: {}", e.getMessage(), e);

            AuthResponse response = AuthResponse.builder()
                    .success(false)
                    .message("Registration failed: " + e.getMessage())
                    .build();

            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
    }

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@RequestBody AuthRequest request) {
        try {
            logger.info("Login request for email: {}", request.getEmail());

            // In production, verify credentials with Firebase Authentication
            // For now, we'll do a simple lookup by email
            // This is a simplified version - you'd need to add email indexing in Firestore

            AuthResponse response = AuthResponse.builder()
                    .success(true)
                    .message("Login successful")
                    .token(UUID.randomUUID().toString()) // Generate proper JWT in production
                    .build();

            return ResponseEntity.ok(response);

        } catch (Exception e) {
            logger.error("Error logging in: {}", e.getMessage(), e);

            AuthResponse response = AuthResponse.builder()
                    .success(false)
                    .message("Login failed: " + e.getMessage())
                    .build();

            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(response);
        }
    }

    @GetMapping("/user/{uid}")
    public ResponseEntity<User> getUser(@PathVariable String uid) {
        try {
            logger.info("Fetching user: {}", uid);

            User user = firebaseService.getUser(uid);

            if (user == null) {
                return ResponseEntity.notFound().build();
            }

            return ResponseEntity.ok(user);

        } catch (Exception e) {
            logger.error("Error fetching user: {}", e.getMessage(), e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    @PostMapping("/verify")
    public ResponseEntity<AuthResponse> verifyToken(@RequestHeader("Authorization") String token) {
        try {
            logger.info("Verifying token");

            // In production, verify Firebase ID token
            // For now, return success
            AuthResponse response = AuthResponse.builder()
                    .success(true)
                    .message("Token verified")
                    .build();

            return ResponseEntity.ok(response);

        } catch (Exception e) {
            logger.error("Error verifying token: {}", e.getMessage(), e);

            AuthResponse response = AuthResponse.builder()
                    .success(false)
                    .message("Invalid token")
                    .build();

            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(response);
        }
    }
}
