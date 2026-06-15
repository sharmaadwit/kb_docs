source_url: https://docs.gupshup.io/docs/message-nodes

<!-- kb-golden:v10 -->
# Message Node JSON Reference

**Module**: Bot Studio

## Definition

Message nodes in Gupshup Journey Builder use JSON structures to define the content, format, and interactive elements of messages. This reference covers all message types with working examples.

## Text Message

**JSON:**
```json
{
  "type": "text",
  "body": {
    "text": "Hello! How can I help you today?"
  }
}
```

## Quick Replies (Buttons)

**JSON:**
```json
{
  "type": "interactive",
  "interactive": {
    "type": "button",
    "body": {
      "text": "Which product?"
    },
    "action": {
      "buttons": [
        {"type": "reply", "reply": {"id": "btn_1", "title": "Electronics"}},
        {"type": "reply", "reply": {"id": "btn_2", "title": "Clothing"}},
        {"type": "reply", "reply": {"id": "btn_3", "title": "Home"}}
      ]
    }
  }
}
```

## List Message With Descriptions

**JSON:**
```json
{
  "type": "interactive",
  "interactive": {
    "type": "list",
    "body": {
      "text": "Choose a category:"
    },
    "action": {
      "button": "Select",
      "sections": [
        {
          "title": "Popular",
          "rows": [
            {
              "id": "cat_1",
              "title": "Electronics",
              "description": "Phones, laptops, gadgets"
            },
            {
              "id": "cat_2",
              "title": "Clothing",
              "description": "Fashion for all ages"
            }
          ]
        }
      ]
    }
  }
}
```

## Carousel

**JSON:**
```json
{
  "type": "interactive",
  "interactive": {
    "type": "carousel",
    "cards": [
      {
        "body": {"text": "Product 1\n$99.99"},
        "action": {
          "buttons": [
            {"type": "reply", "reply": {"id": "p1", "title": "View"}}
          ]
        }
      },
      {
        "body": {"text": "Product 2\n$149.99"},
        "action": {
          "buttons": [
            {"type": "reply", "reply": {"id": "p2", "title": "View"}}
          ]
        }
      }
    ]
  }
}
```

## Common Mistakes

❌ **More than 3 buttons:** Buttons are limited to 3 per message  
✅ **Solution:** Use lists instead for more options

❌ **Button title > 20 chars:** Text overflow  
✅ **Solution:** Keep titles short: "View Details" not "Click here to view detailed information"

❌ **List row description field:** Doesn't display  
✅ **Solution:** Use `description` field inside `rows[]` object

❌ **Descriptions > 72 chars:** Get truncated  
✅ **Solution:** Keep descriptions concise

## Testing

1. Create message node with JSON
2. Use Test Widget in Journey Builder
3. Send to yourself to verify
4. Check on actual device

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Buttons not appearing | Check count ≤ 3, verify JSON syntax |
| List doesn't render | Check ≤ 10 rows, max 3 sections |
| Text cut off | Limit to 2500 chars, use \n for breaks |
| Variables not substituting | Use {{variable_name}} syntax in text only |

## Reference (from source)

<!-- procedural:v2 -->
# Message Node JSON Reference

Complete JSON examples for all message types with troubleshooting.
