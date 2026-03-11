source_url: https://console-docs.gupshup.io/docs/bot-analytics-conversational-path
# Bot Studio Analytics

## Conversational Path

# Conversational Path

## What is the Conversational Path?

The conversation path helps you visualize how your users are moving within different Journeys when conversing with the bot. You can identify major points where users are selecting options or dropping off, and make changes in bot design to improve overall engagement and conversion.

- The display name on the node is the Node Name you have entered on the Bot Studio Journey canvas. If you have not entered the Node Name for a particular node, the node type is shown as the display name.
- If you have not entered the Node Name for a particular node, the node type is shown as the display name.
### It is strongly recommended to enter Node Names on the Journey canvas.

This will help you in identifying the nodes uniquely and distinguish between nodes of the same type when viewing the Conversational Path and the Exit Nodes table.

- At the top of each node, you will be able to see the number of non-cyclic traversals of the respective node. You can hover on the node to know if the node has cyclic traversals.
- The percentage value shows the percentage of traversals on this node compared to the traversals on the previous node.
### The numbers and percentages on each node represent "traversals" i.e. the number of times that node has been triggered.

The number of traversals is not related to the number of conversations or the number of users on a node.

- You will also be able to see the node category on hovering on a node. There are 3 categories of nodes: Bot Response: This category represents a bot message. Customer Response: This category represents a user or customer message. Internal Node: This category represents the Action Nodes and other non-message nodes in your Journeys.
- Bot Response: This category represents a bot message.
- Customer Response: This category represents a user or customer message.
- Internal Node: This category represents the Action Nodes and other non-message nodes in your Journeys.
### If you "Call & Return" a journey from another journey, the nodes and traversals of that journey will appear as a part of the parent journey's Conversational Path.

Let's take an example of a "Journey 2" that is selected in a "Call & Return" node inside "Journey 1". When users traverse from Journey 1 to Journey 2, the first (after Starting Node) node of Journey 2 is attached to the "Call & Return" node of Journey 1, the second node is attached to the first and so on. As a result, the traversals going from Journey 1 to Journey are attributed ONLY to Journey 1, and NOT Journey 2.

### Controls on the Conversational Path

- You can expand a journey to view the later nodes in a Journey using the + buttons present on the right end of each node.
- You can collapse a journey to hide the later nodes in the Journey using the - buttons present on the right end of each node.
## Special Nodes in Conversational Path

### Start Node

- The Start Node indicates the total number of traversals for all the selected Journeys.
- The nodes directly connected to the Start Node represent the actual starting nodes of the respective Journeys.
### Nodes with the Journey Name

- The nodes directly connected to the Start Node represent the actual starting nodes of the respective Journeys and bear the name of the Journey.
- The number highlighted in blue displays the number of traversals entering the Journey represented by the node.
- The percentage value highlighted in blue shows the percentage of traversals entering this Journey from the total number of traversals indicated on the Start Node.
- The number highlighted in red displays the total number of Exits across all nodes in the Journey represented by the node.
- The percentage value highlighted in red shows the percentage of exits entering this Journey from the total number of traversals entering the Journey. This value is capped at 100.00%.
### Exit Nodes

- An Exit is defined as an instance of a user dropping off or not responding to the bot before the session expires.
- Exit Nodes are representations/placeholders of Exits, and not actual nodes in the Journeys.
- These nodes appear at places where users are exiting in a journey and also display the number (and percentage) of traversals in which users have exited at that point in the journey.
- Exit Nodes are always represented in red color with the node name as "EXIT_NODE".
### Cyclic Nodes

- Cyclic Nodes showcase the loops in the bot journey. For example, let's take a journey with 5 nodes - Node 1, Node 2, Node 3, Node 4 and Node 5. If a user at Node 3 has an option to either go to Node 4 or go back to Node 1, Node 3 is displayed with 2 branches - one going to Node 4 and one going to a cyclic node named "Node 1".
- For example, let's take a journey with 5 nodes - Node 1, Node 2, Node 3, Node 4 and Node 5.
- If a user at Node 3 has an option to either go to Node 4 or go back to Node 1, Node 3 is displayed with 2 branches - one going to Node 4 and one going to a cyclic node named "Node 1".
- When the next node in the Journey is already present in the Conversational Path, a Cyclic Node is created in its place.
- A cyclic node bears the name of the original node, but it is differentiated by the loop icon that appears on the node. A tooltip saying "Cyclic Node" also appears when you hover on the node.
- Clicking on the cyclic node redirects the users to the original node already existing in the Conversational Path.
- When you hover on the original node, the number of traversals which have arrived to the node in a cyclic manner appear in a tooltip. The tooltip also provides the total number of traversals (normal + cyclic) on the node.
One node can have multiple cyclic nodes depending upon the Journey design.

### Inactivity Nudges

- Inactivity Nudges are specialized Bot Messages that have been sent to re-engage users after a period of inactivity.
- These nodes represent the Inactivity Nudges feature that you configure through Bot Studio.
- An Inactivity Nudge node bears a clock icon and showcases only the number of times an Inactivity Nudge was sent at its attached node in the journey. Percentage is not applicable for these nodes as they are not a part of the journey.
- Percentage is not applicable for these nodes as they are not a part of the journey.
### The data in Bot Studio Analytics is retained for a period of one year.

Please export required data within a year and store it on your end for later reference.

Updated 10 months ago

- Journey Tracking
