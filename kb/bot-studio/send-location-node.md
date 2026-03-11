source_url: https://console-docs.gupshup.io/docs/send-location-node
# BOT STUDIO

## Send Location Node

# Send Location Node

# Introduction

The Location Node (Message Node) feature allows businesses to share location details with end users via WhatsApp, making it easier to inform them about the business's serviceable locations. This feature is ideal for businesses that need to communicate precise location information to their end users.

# Key Aspects of the Feature

## Functionality

- Address and Location Name (Optional): These fields are optional and can accept either string or number variables, providing flexibility in the data sent.
- Latitude and Longitude Fields (Required): These fields require number values or numeric variables. Only valid number/integer inputs can be mapped to ensure accurate location data. Fill the Latitude and Longitude of the required location to be shared.
# How to Use

- Access the Journey Builder: Navigate to the Journey Builder in your platform and select the flow where you want to add the Location Node.
- Add Location Node: Insert the Location Node (Message Node) into your flow at the desired point where you need to share location information with the user.
- Configure Latitude and Longitude: Enter numeric values manually or map a number variable for Latitude and Longitude. Ensure that only valid number/integer values are used for these fields.
- Enter numeric values manually or map a number variable for Latitude and Longitude.
- Ensure that only valid number/integer values are used for these fields.
- Optional: Configure Address and Location Name: If needed, enter a string or map a string/number variable to the Address and Location Name fields. These fields are optional and can be left blank if not required.
- If needed, enter a string or map a string/number variable to the Address and Location Name fields.
- These fields are optional and can be left blank if not required.
- Save and Deploy: Once the node is configured, save your journey and deploy it. The location will now be sent to users when they reach this node in the flow.
# Use Cases

### Service Area Notifications

- Scenario: A delivery service wants to inform customers about their delivery areas by sending the exact coordinates of serviceable zones.
- Benefit: By using the Location Node, businesses can efficiently communicate geographical information, ensuring that end users know whether they are within a serviceable area.
### Store Location Sharing

- Scenario: A retail chain wants to share the exact coordinates of a new store location with customers on WhatsApp.
- Benefit: The Location Node allows the business to send accurate latitude and longitude details, along with optional store names and addresses, making it easy for customers to locate the store.
Updated 10 months ago
