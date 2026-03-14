source_url: https://console-docs.gupshup.io/docs/teams






<!-- agent-assist-golden:v10 -->
# User Management: Teams

**Module**: Agent Assist

## What this feature does
Use **Teams** to group agents under a supervisor and define the **assignment policy inside a team** (e.g., Round Robin vs Load Balancer). Teams define **who belongs together**; they don’t define the full routing rules for every incoming chat.

## Exact UI path
Agent Assist → Settings → User Management

## Setup path
- Navigate to the settings tab on your dashboard.

## Steps
1. Open Agent Assist.
2. Navigate to the settings tab on your dashboard.
3. Click **Save** to apply changes.
4. Click "Add New Team" and provide the team name.
5. Select a supervisor for the team from the dropdown list.
6. Add executive users/agents to the team by selecting them from the dropdown.
7. Choose between "None," "Load Balancer," and "Round Robin" for assignment type.

## Validation / where to check
- _Run a quick test (new chat / assignment / workflow) and confirm expected behavior._

## Fields to configure
- Add New Team
- Team name
- Supervisor
- Agents (members)
- Assignment type (None / Load Balancer / Round Robin)

## Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy** if available) to apply changes.

## Troubleshooting
- _Add common failure modes and how to fix them._

## Prerequisites
- _List required roles/access, teams, and any upstream configuration._

## Options / variants
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflow docs
- _Link this feature to adjacent modules (e.g., Business Hours ↔ Auto Replies; Assignment Rules ↔ Teams ↔ Views)._

## Module disambiguation docs
- **Teams** define group membership + per-team assignment policy.
- For **conditional assignment** (based on channel/tags/priority) to teams/agents, use **Settings → Chat Management → Assignment Rules**.

## Reference (from source)
### Overview
Section 1: Adding Users to Teams

### When to use
_Add the primary scenarios and personas._

### Details
Section 1: Adding Users to Teams

Creating and Configuring Teams

To add users to teams within Agent Assist:

Step 1: Access the Teams Settings Page

- Navigate to the settings tab on your dashboard.
Step 2: Creating a New Team

- Click "Add New Team" and provide the team name.
- Select a supervisor for the team from the dropdown list.
Step 3: Adding Executive Users/Agents to the Team

- Add executive users/agents to the team by selecting them from the dropdown.
Step 4: Specifying Assignment Type

- Choose between "None," "Load Balancer," and "Round Robin" for assignment type.
Step 5: Choosing Business Hours

- Define the business hours for the team, specifying when the team operates and when chats will be assigned to it.
Section 2: Difference Between Round Robin and Load Balancer Assignment

Assignment Type Distinctions

- Round Robin Assignment: Chats are assigned automatically to available agents without limits.
Round Robin Assignment: Chats are assigned automatically to available agents without limits.

- Load Balancer Assignment: Chats are assigned based on specified limits for each agent, including Open, Pending, and Awaiting Response chats. Agents are assigned chats according to the limits set. (To understand how to configure load balancer assignment, please refer to thislink)
Load Balancer Assignment: Chats are assigned based on specified limits for each agent, including Open, Pending, and Awaiting Response chats. Agents are assigned chats according to the limits set. (To understand how to configure load balancer assignment, please refer to thislink)

Section 3: Default Team Settings

Efficient Default Team Configuration

The default team automatically adds all users when they are added. The assignment policy for the default team is round robin assignment to all agents, and it is mapped to default business hours. This ensures that all incoming chats are assigned to agents in a round-robin manner without the need for further configuration.
