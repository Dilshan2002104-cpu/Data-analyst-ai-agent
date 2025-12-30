package com.dataanalyst.backend.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SQLConnection {
    private String id;
    private String userId;
    private String name;
    private String type; // mysql, postgresql
    private String host;
    private int port;
    private String database;
    private String username;
    private String password; // Stored as plain text for now as per plan
    private String createdAt;
}
