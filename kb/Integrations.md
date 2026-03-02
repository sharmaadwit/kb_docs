# Integrations

## Native Platform Integrations

## Connector Marketplace

## Custom Webhook Setup

## Leveraging Events

Hello and welcome to Gupshup Academy. In today\'s session, we are going
to cover integrations. So, we\'ll going to cover the console
integrations. So before we talk about console integration, we majorly
have three kind of integrations. One is the native integration which you
can currently look at on the screen which we have with MoEngage,
CleverTap and Shopify. I\'ll talk about it in depth. Then we also have
connectors available with leading CRMs, ERPs, and Martech platform. To
know more about them, you can go to this page particularly
gupshup.io/integrations/connectors. You can just search about any of the
connectors like which you are looking at and you\'ll be able to know
that which kind of connectors we have with these systems available. Okay
coming back, when it comes to integrations with MoEngage, CleverTap and
Shopify, which are Martech and e-com platform, how this works is that,
for example with MoEngage, we enable customers to easily and seamlessly
launch campaigns directly from the MoEngage account. The steps in
configurations are super simple, it just happens with a click. We have a
detailed document available here which talks about MoEngage integration
in depth. Similarly when it comes to Shopify, we have, you know, we
enable businesses to send important events or attributes to Gupshup
which subsequently can be used for sending out personalized campaigns.
So majorly if you want to understand the events which we cover in
Shopify integration, these are order fulfillment, order placement,
cancellation, abandoned cart or checkout reminders. And then this
integration can also be achieved by just the configuration and the
entire details about MoEngage, Shopify and CleverTap is available in
this thread. So if you want to know more about that, you can look at
CleverTap integration, MoEngage or Shopify from this thread itself.
Okay, coming back, after that we do have also one thing called custom
integration. Now how custom integration works is that and what is the,
you know, understanding of custom integration? So now apart from
MoEngage, CleverTap or Shopify, if a business wants to send or pass
event from any of the external systems which can be their CRMs, it can
be their website, we can actually pitch them or we can give them a
custom integration solution. Now once we receive those events, we can
actually leverage these event in different modules in our console
platform which we will shortly look at. Now how this entire structure
works obviously you also have a detailed document available on how
custom integration works. I\'ll quickly talk about it, so let\'s look at
by creating clicking on creating a custom integration, once you click on
that, you just have to name your custom integration. So we\'ll just keep
a name like test_academy for now and then you just have to define the
JSON path here as well which also acts like a unique event identifier.
Now once you come here at this particular page, you will see the two
different details here. One is the callback URL which will be generated
and the authorization token. So callback URL obviously is a webhook
through which the event data can be passed on and the authorization
token is for URL authentication. Obviously if you want to also or
developers also want to look at the payload structure, the sample JSON
can be seen over here. And if you see here this is the place wherein we
can actually add the events. So once you\'ll click on an add event, by
default these two events will come up. For example let\'s suppose we are
looking at creating a lead generation event. Right, so or a signup
event. So let\'s suppose if somebody signs up on a website or in mobile
app, we want to pass that event to our platform. So we can put in any of
the unique identifier. Apart from having the default, you know, property
type which is data type which can be text or timestamp, we can actually
add property. For this we can actually name a property called, you know,
test and we can actually also select if this property type can be a
number, text, decimal or whatever. So we can just select it like this
and we can just create an additional property. Here we are creating a
signup event and we can actually save this event here after creating it.
So yeah, so once we do that, how do we leverage these events is that
obviously once you create the event and do the configuration, you can
use this event either in the Bot Studio. In the Bot Studio, you can just
simply use this event to trigger automated message once the signup event
has happened. So imagine once a customer signed up on a website,
automated message can be triggered to customer on WhatsApp. And
similarly you can also leverage this in our personalize layer or
personalize module wherein in case if you want to pass this customer
event and update any property about that user or customer, it can also
flow in through the event section here. So if you see here in the event,
whatever new events you are creating will get listed here and that can
subsequently be mapped across the profiles in the personalized layer.
Yeah. For more details as I said, if you go to the integration section,
you\'ll get to see detailed documentation available which can help you
to understand in more detail about how this integration works. I hope
this was helpful. Thank you so much.
