# Terminal Breakfast Shop

## Objective

Implement a multi-terminal TUI system that simulates the complete workflow of a breakfast shop - from order placement to preparation to payment confirmation. The system consists of three terminal entry points:

- Display board terminal (read-only)
- Customer ordering terminal (interactive)
- Shop owner management terminal (interactive)

## Ports and Role Requirements

1. **Display Board Terminal**: ssh localhost:8824
    - Read-only
    - Auto-refreshes current queue number, preparation status, and payment status
2. **Customer Ordering Terminal**: ssh localhost:8825
    - Supports multiple simultaneous connections
    - Each connection receives a queue number
    - Allows placing orders and displays a payment QR code (mock acceptable)
3. **Shop Owner Terminal**: ssh localhost:8026
    - View the order list
    - Update order status (pending payment / paid / preparing / etc.)

## Technical Constraints (Required Reading) emnew Im

You may use a self-built SSH/Telnet or other terminal protocol solution, but you must describe the architecture.

## Functional Requirements (Mandatory)

- All terminals share the same order state; state changes must be visible in real time.
- Order state transitions must be valid (illegal transitions are forbidden).
  The customer terminal must support basic menu browsing and order placement.
- The owner terminal must support updating order status by order number.

## Testing and Acceptance Requirements (Mandatory)

Execute and record results for at least the following tests:

1. Multi-connection test
2. State transition test Reacted 19 your message 2th
3. Disconnection recovery test
4. Concurrent consistency test

## Deliverables

- Server and client source code
- One-command startup script
- Terminal operation guide (keyboard shortcuts / commands)
- Test scripts and results
- Architecture description (protocol selection, state synchronization approach)

## Bonus Points

- Persistent storage
- Basic access control
- Highly readable TUI interaction design
