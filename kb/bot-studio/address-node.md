source_url: https://console-docs.gupshup.io/docs/address-node

<!-- procedural:v2 -->
# Address Node

**Module**: Bot Studio

## Overview
Address Node

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Address Node

# Introduction

The Address Node enables businesses to send an address form to users via WhatsApp, streamlining the process of collecting user address details. This functionality is tailored for WhatsApp Business Accounts (WABAs) in India and Singapore, providing region-specific forms for efficient and user-friendly interaction.

# Key Aspects of the Feature

- Region-Specific Availability: Supported only for India and Singapore WABAs. Not functional for other regions; bot designers must select the appropriate region during configuration.
- Supported only for India and Singapore WABAs.
- Not functional for other regions; bot designers must select the appropriate region during configuration.
- Dynamic Form Parameters: Users receive a form with fields specific to the selected country. Ensures compliance with regional address standards.
- Users receive a form with fields specific to the selected country.
- Ensures compliance with regional address standards.
- Seamless User Input: Users can input their address directly in the WhatsApp form. Data is returned to the bot for processing or storage.
- Users can input their address directly in the WhatsApp form.
- Data is returned to the bot for processing or storage.
# How to Use

- Node Setup: Add the Address Node to the journey in the Journey Builder. Configure the node by selecting India or Singapore as the WABA region.
- Add the Address Node to the journey in the Journey Builder.
- Configure the node by selecting India or Singapore as the WABA region.
- Form Configuration: The form will dynamically adjust based on the selected region. Available parameters for each country will be displayed automatically.
- The form will dynamically adjust based on the selected region.
- Available parameters for each country will be displayed automatically.
- Deploy and Collect: Deploy the journey. Users will receive the address form on WhatsApp, input their details, and submit.
- Deploy the journey.
- Users will receive the address form on WhatsApp, input their details, and submit.
- Error Handling: For unsupported regions, the bot designer must configure fallback logic or alternative messages.
- For unsupported regions, the bot designer must configure fallback logic or alternative messages.
### Sample Payload for Pre-Filled Values:

```
{
             "name": "CUSTOMER_NAME",
             "phone_number": "9898989898",
             "in_pin_code": "666666",
             "address": "Some other location",
             "city": "Delhi"
          }
```

### Sample Payload for Saved Address:

```
[
    {
      "name": "John",
      "address": "22B Baker Street",
      "city": "Bengaluru",
      "state": "Karnataka",
      "addressId": "xyz",
      "phoneNumber": "+919999999999",
      "pinCode": "777888",
      "houseNumber": "1",
      "floorNumber": "2",
      "towerNumber": "30",
      "buildingName": "4",
      "landmark": "landmarkArea",
      "postalCode": "8080",
      "addressLine1": "addressLine1",
      "addressLine2": "addressLine2",
      "country": "IN"
    }
  ]
```

### Sample Payload for Validation:

```
{
    "name": "Invalid Name",
    "address": "Wrong address",
    "city": "Invalid city",
    "state": "Invalid state",
    "phoneNumber": "Invalid Phone Number",
    "pinCode": "Invalid Pin",
    "houseNumber": "Invalid houseNo",
    "floorNumber": "Invalid FloorNo",
    "towerNumber": "Invalid TowerNo",
    "buildingName": "Invalid Building Name",
    "landmark": "Invalid Landmark",
    "postalCode": "Invalid Postal Code",
    "addressLine1": "Invalid address line1",
    "addressLine2": "Invalid address line2",
    "country": "Invalid country"
  }
```

# Use Cases

- E-commerce Order Fulfillment: Scenario: An e-commerce business collects customer shipping addresses via WhatsApp. Benefit: Simplified address collection ensures quick and accurate data for timely deliveries.\
- Scenario: An e-commerce business collects customer shipping addresses via WhatsApp.
- Benefit: Simplified address collection ensures quick and accurate data for timely deliveries.\
- Service Appointment Scheduling: Scenario: A service provider collects location details for home services. Benefit: Address Node ensures smooth address input, improving operational efficiency.\
- Scenario: A service provider collects location details for home services.
- Benefit: Address Node ensures smooth address input, improving operational efficiency.\
- Event Registration: Scenario: An event organizer gathers venue-specific participant addresses. Benefit: A WhatsApp-based form enhances the user experience while ensuring accurate location data.
- Scenario: An event organizer gathers venue-specific participant addresses.
- Benefit: A WhatsApp-based form enhances the user experience while ensuring accurate location data.
## NOTE

- The Address Node is restricted to India and Singapore WABAs.
- For other regions, alternate workflows or fallback logic must be configured.
This Address Node simplifies user address collection via WhatsApp while tailoring the experience to specific regions, enhancing operational efficiency and user satisfaction.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Deploy and Collect: Deploy the journey. Users will receive the address form on WhatsApp, input their details, and submit.
- - Deploy the journey.
- - Users will receive the address form on WhatsApp, input their details, and submit.

**Last updated (from source)**: Updated 10 months ago
