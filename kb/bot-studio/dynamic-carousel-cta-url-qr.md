source_url: https://console-docs.gupshup.io/docs/dynamic-carouselcta-url-qr

<!-- procedural:v2 -->
# Dynamic Carousel (CTA URL + QR)

**Module**: Bot Studio

## Overview
Dynamic Carousel allows businesses to send Horizontal list of card containing media, title, subtitle and Button (QR/CTA URL)

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
# Introduction:

Dynamic Carousel allows businesses to send Horizontal list of card containing media, title, subtitle and Button (QR/CTA URL)

In addition, you can send Quick Reply and CTA URL buttons on each card making it a more flexible and customized experience for the users. This allows the end users to click a URL based button to visit the business website or select a QR Button for the same card to continue the conversation.

## New Upgrades for Dynamic Carousel (CTA URL + QR)

Quick Reply Buttons on Each Card:

- Allows users to respond directly within the conversation using predefined response options.
- Enhances user interaction and provides a more seamless conversational experience.
CTA URL Buttons on Each Card:

- Each card can now have a CTA button linking to a specific URL.
- Users can click the URL-based button to visit the business website or a specific landing page for more information or actions.
## How to use the feature:

The 'Dynamic' feature is very easy to use. The steps are given below

Steps:

- Toggle on the 'Dynamic' switch of the Carousel node.
- After turning on the 'Dynamic' mode, the toggle switch for button will appear. Now turn on the 'Dynamic' switch here.
- And now choose the 'Dynamic' button type from here.
When URL or Payload option is selected, then all the buttons become the same type. For example, if URL is selected then all the buttons will be URL type.

But now with the dynamic option, the flexibility to choose URL or Payload on each button is available. For this it is important to provide 'type' & 'value' field in the JSON.

For making the button payload type:

"type": "postback"

"payload": "value"

For making the button URL type:

"type": "URL"

"URL": "value"

For reference, see the sample given below:

Sample Payload which you can use:

```
{
  "carousel": [
    {
      "image": "https://picsum.photos/200",
      "bodyTitle": "Title of the Card1",
      "bodysubTitle": "Subtitle of the Card1",
      "buttons": [
        {
          "title": "Buy",
          "type": "postback",
          "payload": "card1_yes"
        },
        {
          "title": "Book Test Drive",
          "type": "postback",
          "payload": "card1_no"
        },
        {
          "title": "Know More",
          "type": "url",
          "URL": "https://gupshup.io"
        }
      ]
    },
    {
      "image": "https://picsum.photos/200",
      "bodyTitle": "Title of the Card1",
      "bodysubTitle": "Subtitle of the Card1",
      "buttons": [
        {
          "title": "Buy",
          "type": "postback",
          "payload": "card1_yes"
        },
        {
          "title": "Know More",
          "type": "url",
          "payload": "https://gupshup.io"
        },
        {
          "title": "Know More",
          "type": "url",
          "URL": "card1_know"
        }
      ]
    }
  ]
}
```

You can form the JSON in the expected format and pass it in a JSON Variable to refer the same in the Dynamic Carousel Element field:

Further instructions on how to fill the node with the payload variable can be found here - How to use a Dynamic Carousel?

## Use Cases:

Dynamic Carousel with CTA URL & Quick Reply feature can now significantly improve experience for the users giving the businesses more flexibility with customization. Here are several use cases that demonstrate the potential applications of the new features in Dynamic Carousel:

1. E-commerce Promotions

Scenario: Showcasing new product collection. Dynamic Carousel: Display product cards with "View Details" (CTA URL) and "Add to Wishlist" (Quick Reply) buttons. Benefit: Increases engagement and simplifies the shopping experience.

Scenario:Personalized product recommendations. Dynamic Carousel: Use quick replies to filter products based on user preferences. Benefit: Enhances user interaction and satisfaction.

2. Event Marketing

Scenario: Promoting conference sessions. Dynamic Carousel: Display session cards with "Register Now" (CTA URL) and "Show More Info" (Quick Reply) buttons. Benefit: Boosts visibility and registration rates.

Scenario: Post-event engagement. Dynamic Carousel: Send feedback requests via quick replies after event attendance. Benefit: Collects valuable insights to improve future events.

3. Service Booking

Scenario: Booking salon services. Dynamic Carousel: Display service cards with "Book Now" (CTA URL) and "Request Callback" (Quick Reply) buttons. Benefit: Simplifies the booking process and improves customer experience.

Scenario: Promoting new services. Dynamic Carousel: Highlight new services with detailed descriptions and quick reply options for more info. Benefit: Increases awareness and bookings.

4. Content Distribution

Scenario: Sharing blog posts. Dynamic Carousel: Display content cards with "Read More" (CTA URL) and "Subscribe" (Quick Reply) buttons. Benefit: Drives traffic to the website and encourages subscriptions.

Scenario: Engaging with newsletter subscribers. Dynamic Carousel: Send curated content to subscribers using quick replies for more targeted engagement. Benefit: Boosts reader interaction and loyalty.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
