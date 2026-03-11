source_url: https://console-docs.gupshup.io/docs/dynamic-image-url-node
# BOT STUDIO

## Dynamic Image URL Node

# Dynamic Image URL Node

### When to Use

The Dynamic Image URL Node can be used to create dynamic images during run-time. The dynamic card image can be stored in a variable and sent to the user using an Image Node. For instance, the business wants to send QR Code to customers with dynamic information of the customer, the dynamic image card can be created and sent to the user. This can be used to send movie tickets or banking statements to users.

### How to Use

Drag and drop the Dynamic Image URL Node on the canvas.

- Select one of the three templates and fill the content. TemplateTemplate ContentTemplate 1Card titleSubtitleDescriptionImage(16MB)Image(16MB)Template 2Card TitleSubtitleImage(16MB)DescriptionTemplate 3Card TitleSubtitleDescriptionImage(16MB)
Select one of the three templates and fill the content.

All headers within a template are mandatory.

- Preview the template as it would be sent on the channel from the node on the canvas.
- Save the image in a string variable and bot designer can use a reply node or image node to send the dynamic card image URL to the channel.
### Limitations:

- Three pre-defined templates are available in the dynamic card image URL node
- A message node can send the image URL to the channel.
Updated 10 months ago
