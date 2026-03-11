source_url: https://console-docs.gupshup.io/docs/carousel-and-lto-template-support-via-send-message-node
# BOT STUDIO

## Carousel & LTO Template

# Carousel & LTO Template

Carousel & LTO Template via Send Message Node. Available for JB Pro only.

# Introduction:

Journey Builder Pro now allows businesses to send Limited Time Offer and Carousel Templates during two-way conversations. This is made possible using the Send Message Node on the Journey Builder canvas. Bot designers can request dev access to use the Send Message Node for their project.

# How to use the feature:

Select the Text/Template option on the send message node and use the below sample payload format for reference. Designers can dynamically create the Payload in the same format mentioned below to send customized Templates during bot runtime.

# Sample Payloads:

## Limited Time Offer -

```
 {
    "type": "text",
    "template": "{\"id\":\"<<GUPSHUP_TEMPLATE_ID>>\",\"params\":[\"<<COUPON_CODE>>\"]}"
  }
```

## Carousel -

```
{
  "type": "text",
  "template": "{\"id\":\"<<GUPSHUP_TEMPLATE_ID>>\",\"params\":[]}",
  "message": "{\"type\":\"carousel\",\"cardHeaderType\":\"IMAGE\",\"cards\":[{\"link\":\"https://env1-common-marketing-bucket.s3.amazonaws.com/31252338/31563891/20/e4189ec7-36df-43fb-a79c-c8101dcd76cf/Media_Image_3.jpg\"},{\"link\":\"https://env1-common-marketing-bucket.s3.amazonaws.com/31252338/31563891/20/e4189ec7-36df-43fb-a79c-c8101dcd76cf/Media_Image_3.jpg\"}]}"
}
```

Updated 8 months ago
