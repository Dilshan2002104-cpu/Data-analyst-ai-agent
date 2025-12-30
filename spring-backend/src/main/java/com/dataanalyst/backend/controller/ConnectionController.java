package com.dataanalyst.backend.controller;

import com.dataanalyst.backend.model.SQLConnection;
import com.dataanalyst.backend.service.FirebaseService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/connections")
@CrossOrigin(origins = "http://localhost:5173")
public class ConnectionController {

    private final FirebaseService firebaseService;

    public ConnectionController(FirebaseService firebaseService) {
        this.firebaseService = firebaseService;
    }

    @PostMapping
    public ResponseEntity<SQLConnection> saveConnection(@RequestBody SQLConnection connection) {
        try {
            // Ensure ID exists
            if (connection.getId() == null || connection.getId().isEmpty()) {
                connection.setId("conn_" + UUID.randomUUID().toString());
            }
            // Ensure timestamp
            if (connection.getCreatedAt() == null) {
                connection.setCreatedAt(Instant.now().toString());
            }

            SQLConnection saved = firebaseService.saveConnection(connection);
            return ResponseEntity.ok(saved);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }

    @GetMapping("/{userId}")
    public ResponseEntity<List<SQLConnection>> getUserConnections(@PathVariable String userId) {
        try {
            List<SQLConnection> connections = firebaseService.getUserConnections(userId);
            return ResponseEntity.ok(connections);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }

    @DeleteMapping("/{connectionId}")
    public ResponseEntity<Void> deleteConnection(@PathVariable String connectionId) {
        try {
            firebaseService.deleteConnection(connectionId);
            return ResponseEntity.ok().build();
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }
}
