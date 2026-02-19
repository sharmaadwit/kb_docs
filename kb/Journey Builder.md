# Journey Builder

Hi, Good Morning, Good Afternoon, Good Evening, I\'m not sure what part
of the day are you watching this video in. All right, so my name is
Purusottam, also known as Puru, I\'m part of the pre-sales team and in
this video, I\'m gonna talk about the journey builder. All right, so
let\'s get started, let me log in to the converse platform. Okay, select
the org and here we are, here we are with Gupshup sales as a project
over there. All right, so I\'m pretty much sure you\'ve seen all of
this, you\'ve seen the platform before. Let\'s quickly dive into the

## Understanding Journey Types

Journey Builder. So under Bot Studio, you'll find multiple subsections,
Journeys is the place where you need to focus on. All right, so journeys
can now be of three types, User initiated as in the user comes to our
channel or chatbot or our agent and types in hi or hey or whatever,
doesn\'t matter, but user comes to the conversation and that\'s user
journeys. Then there is Campaign Journeys, basically the brand initiates
the conversation, the brand sends out that particular message on
WhatsApp, on RCS or any given channel where in push notification and
two-way conversations are possible. So the brand sends that message and
then we link it then if the customer replies back. For example if let\'s
say we send out a communication, a promotional message from a bank to a
customer that you\'re eligible for this particular card and there\'s
this reply button on top of it which says apply now. So as soon as the
user clicks on apply now, a campaign journey gets initiated, right? And
then there there are Ad Journeys, basically I\'m sure you have you have
heard of C2WA click to WhatsApp. So now customers coming in from
Facebook, Instagram, TikTok or even Google, Google ads can be redirected
to WhatsApp and as soon as they\'re on WhatsApp, there\'s this ice
breaker which gets configured, which gets auto populated on the text box
of the customer\'s phone and as soon as the user sends that particular
message, a journey gets triggered. So now specific ads can be mapped to
specific journeys and those are ad journeys. Now you must be thinking
why these three categories? Pretty simple. For example let\'s say Apply
Now, this is the keyword that we map to user journeys and whenever a
user says Apply Now, a journey starts starts off, but there could be a
campaign campaign message as well which has been sent out to the
customer which says apply now. Or maybe a brand has sent three different
promotional messages one for credit card, one for an FD offer and and
one for a debit card offer. All of them contain the same title which is
apply now. So if we do not have this segregation if we do not have these
these mappings here, then the bot or the agent would get confused right?
I mean which apply now which journey to be triggered? Hence the
bifurcation hence we have kept three different categories of journeys
here making it making it more simpler and easier for the bot designer to
go ahead and have a pinpointed conversation with the end user. So now
what you see on your screen I\'ll just refer to user journeys mostly
journey creation for every given every given subcategory over here is
the same. There\'s no difference between journey creation or there are
no extra let\'s say nodes or steps or types of messages which are
available in one kind of journey and not the other. Everything remains
similar, right? So okay, so all of these line items which you see,
please ignore the names of them, these are individual journeys, right?
So I\'m going to stick to the same example here. For example, we are
creating a banking bot let\'s say a WhatsApp banking bot for example,
then

## Modular Architecture Principles

the journey builder is designed in such a way that we could we
should keep each journey separate. What I'm trying to say is let's say
there is a balance inquiry journey, that is a separate line item here
and then there is fund transfer which is a separate line item line item,
then there could be open FD and so on and so on, right? So we'll have I
mean the journey builder is designed to go ahead and give a modular
nature to the end to the backend of a particular bot that we create.
Why? Because it\'s obvious that it will get easier to maintain these
journeys without so it\'s it\'s very similar to microservices in the
software development and monolithic architecture. If it is monolithic
every small change might take more time because it it might affect other
functionality but if we keep things modular, of course it gets easier to
maintain and implement, right? So I\'ll go back a step. Yeah, so you\'ve
got three things here I\'ve I\'ve obviously got developer mode access
over here hence I\'m able to see database, but for a general user also
there is this test bot so as soon as you create a particular journey,
you\'ll be able to test it right here on this particular bot. So let\'s
create a journey. Once a user or a bot designer clicks on this
particular button, they get all of these options here, I mean these
options are nothing but predefined templates which the user or the bot
designer could readily pick up and start the development, right?
Obviously I mean the user would not have to start from scratch rather
the user could select from each of these journeys here. So let\'s say I
want to do a lead generation journey. Right, so I\'ll just zoom out. Now
what you can see is is a flowchart here, right? Different blocks
connected together with the arrow mark on it and it goes towards from
the start to the end over there, right? Now let\'s zoom in and see what

## Designing with Nodes (Prompt/Message/Action)

exactly these steps are. So basically every particular journey will have
a start node. This start node is nothing but this tells the bot to
trigger which particular journey at which given time, right? So for
example there could be a user input, right? If someone enters balance
inquiry or something like that, or let\'s say apply now, some keyword
you can keep adding these keywords you can have different operators in
here which could help trigger this particular journey. So the primary
idea is that starting node gives you the agility to go ahead and map
whatever input or event do you want the journey to be triggered at?
Okay, so it could be user input, it could be AI trigger, maybe we train
an intent we\'ll obviously look at other modules of bot studio wherein
AI admin is a piece wherein you could train intent and then after
instead of sticking to just two or three keywords to trigger a
particular journey, the bot could actually be a little more intuitive
and understand the user intent. For example if someone comes to the
banking bot same banking bot and says what\'s my balance, it will be
able to understand it and trigger this particular journey or I want to
apply for a credit card then that intent will get triggered and the
particular journey would be rendered in front of the customer on
whatever channel it is, right? Be it WhatsApp or others. Okay, so
that\'s starting node but then after defining what triggers this journey
you\'ll have to define the steps of the journey there right? So the very
first one is over here in this template it is welcome to the support
journey, please help me with the following details. The very first one
is we are asking for name, then we are asking for phone number and you
can see the connections between the journeys over there. Now we I mean
we continue to ask all of those questions basically whatever questions
we want the bot to ask to the end user while in while in runtime while
the user is availing this service on a particular chatbot, this is how
it is done, right? Now let me show you what are other options are
available for a bot designer to go ahead and use while they\'re crafting
that journey out. It could be a simple text message simple as that. It
could be an image or an audio file which could be rendered in front of
the customer similarly it could be a reply button you must have seen a
lot of examples of these this is basically nothing but a card like
template wherein there is a header it could be a image video or
something then there is a body and there are buttons, right? Similar to
what we have normally on WhatsApp promotional message which is sent out
to the customers most of the brands do it, right? You send out a message
which has a header as a as a media file and then there is the body which
explains the offer or whatever it is and then there are CTA buttons at
the bottom. Similar to that in the bot journeys you could have such
stuff and then there could be a list, a quick reply all of that of
course you can go ahead and filter it out basis the channel that you\'re
defining the journey for. It could be send location you can ask for a
location of a particular customer, it could be WhatsApp flows we\'ll
talk about WhatsApp flows in a bit. I\'ll I\'ll be making another video
for it in which I\'ll try and make you understand how a WhatsApp flow
journey is built on console, right? So that\'s that\'s the message
section and then we have actions, basically these are the actions the
bot will perform if the user goes through a specific branch of a
particular journey, right? So we can define conditions basis which the
logic could change, we can connect different journeys with the help of
call and return as I was saying earlier, right? That we\'ll have to I
mean keep it modular, balance inquiry is one journey, fund transfer is
another. So basically I mean as a whole it it is irrelevant to the end
user that whether you keep it monolithic or if you have modular nature
in your backend but eventually we\'ll have to go ahead and give the user
a seamless experience by connecting these journeys together, right? And
that\'s that\'s when call and return comes into the picture at whatever
step in a particular journey you want to trigger another journey or
connect that journey you could bring it use this particular node.
Similarly there is agent transfer which is nothing but as soon as the
journey reaches this particular step an automatic chat will be created
in the agent assistant panel and the human touch could be brought in,
right? So there are of course I mean we cannot have static or journeys

## Handling API Integrations

which don't change as per the user user ID or user per user over there,
right? For example my balance could be something else, your balance
could be something else and that would require certain API integrations
as in this data resides on the bank server and Gupshup has no clue of
it. So in order to go ahead and fetch that piece of information and put
it in front of the customer we'll need an API call and that API call
could be defined wherever wherever in the journey we want to trigger it,
so basically to pull and push information from this journey into the
client's backend is something which can be done using API block. The
API block is basically an emulation of nothing but the popular software
called Postman, basically the software is used to go ahead and test
different kinds of APIs especially the REST APIs over there with so
basically you can either import the entire Postman collection over here
and then configure it wherever you want or you can build it ground up
from here or you can even import the curl and put it right here. So all
of the options mostly whatever whatever options are available to a
developer in a IDE or in in Postman similar to that we've kept it here,
right? Now that's that's API block but then again there could be
certain business logics which cannot be defined using conditions and
call and return it might take it might be a very tedious to do so with
that function so in that case we'll bring in the code block basically
there is a whole ID in place kind of like a JavaScript editor wherein
you can write your JavaScript code and these code blocks can be can have
small snippets of code and can be connected at the relevant step in the
journey so that while in runtime if the user chose to click on that
button the code gets executed otherwise it doesn't and the relevant
outputs are given to the end customer. Now after that there are prompts
now there are certain questions which are pretty generic and are being
used in most of the journeys over there, right? So for example let's
let's take an example of phone, right? We might need the phone number
of the customer and this is needed to identify the customer in many of
the use cases and the journeys over there. So for those kind of stuff
wherein it's I mean we can use ready to use blocks basically phone
number, email, date, number, location request, address, all of that and
these come up with predefined validations also, right? For example a
number could this is a regex nothing but a regular expression which has
been defined, so in case the input of the user satisfies this expression
only then the bot will allow the user to go to the next step. This this
I mean I'll just try to explain this very simply this is nothing but a
a the validation which counts how I mean how many digits are there in a
particular number. So let's say the user entered a nine digit number,
it will not accept it it will need 10 digits so that's that's what is
being defined here. Other than that how many retries can can be given to
the user that is can be also be defined, you can define the failure
message as well let's say the user entered a wrong number so at that
particular time you can say my apologies apologies the number is wrong
please enter the correct number or something like that. So the the
definition of prompts is basically these are messages only but with a
predefined purpose with a predefined thing which are generally used in
many of the journeys there just to make the bot designer's life easy
it's prebuilt you just drag and drop it and it starts to work. Then
there are blocks now prompts are predefined preconfigure messages
nothing but messages which can be used one at a time, right? But let's
imagine that we are building building two three journeys in place and
there could be multiple API calls which are common for these journeys.
For example I mean I'm taking a very technical example here but let's
say let's say we're building the same banking bot, right? And to fetch
to call the API of the customer the banking as in the balance inquiry
API of the customer before that we'll have to call the authentication
API to generate a token and that token needs to be fed to every given
API be it the balance inquiry API be it the be it the fund transfer or
opening an FD all of those APIs will require that authentication token.
Now if we go ahead and try configure this particular API in every given
journey it might be time consuming. So whatever journeys whatever steps
that are common for that are common for which are common for multiple
journeys the bot bot designer can simply go ahead and create a block out
of it, okay? Basically create a block out of it and then use that block
across different journeys whatever he or she is creating over there,
right? So you can name this block and then this will be saved in the
journey builder and whenever there is a need that could be used. So let
me just maybe show you this the pre-existing blocks are like this
prescription block or maybe the AI block let me pull this up from here
and it says it has number three nodes I expand it, right? I expand it
these are the num let's say I want to use these things here, right? So
what I'll do is I'll simply drag and drop the block here and then
I'll connect it to my existing journey somewhere like this maybe I'll
pick this one here and put it right here and it gets connected, right?
And then I mean basically reuse of just like how we have reusability of
code here here we have reusability of journeys as well. So that's
pretty much it just one more thing I would like to cover so while we are
building a journey let's say we are building this particular journey
right lead generation journey we ask for name, phone number, email,
other things, right? So before we push it to their backend for example
maybe we have an API here which pushes all of this collected information
from the bot to their CRM, right? Now in order to push this data we'll
need to temporarily at least store it somewhere the name of the
customer, the phone number and other details that we have collected
we'll have to store it somewhere in the journey before pushing it to
the API and once we have push it to the CRM or the relevant system we
delete it from here. So what I mean to say is while in the runtime of
the journey while the user is executing the journey till we reach the
last step wherein we are pushing the data to their systems we'll need
to temporarily store it somewhere and that's that's when variables
come into the picture, we go ahead and store pieces of information from
the journey from external systems from pre-existing knowledge all of
those over here and use it in the journeys wherever you want. So there
are three three kinds of variables four kinds of variables local,
global, system and constant. Local as the name suggests you'll use this
within the journey that you've defined the value will not be accessible
outside the journey, okay? Now then there is global, global is basically
let's say you've saved a particular value in a particular global
variable then that variable's value the data would be accessible in all
of the journeys that you've created balance inquiry so I was taking the
exam example of authentication token of the API so basically we'll call
that API we'll store it in global variable and then after it will be
usable throughout whatever journeys wherever we want to call those APIs
there. So that's global wherein you want to share data, then there are
system variables so certain attributes of the customer comes in
automatically not automatically of course we have built the journey
builder that way that it fetches some pieces of information readily
without even asking the customer for it. For example user channel ID
this thing this is nothing but if the user is on WhatsApp let's say for
example then as soon as the user says Hi and the bot starts to respond
back and the journey builder takes the control in every given journey
this user channel ID will have the phone number of the customer. Now if
at all I step we'll have to ask the user for their phone number
rather asking we can pick it from here it will automate the journey it
will it will reduce one more touchpoint for the end user and it will
make their lives easier. So there are several system system variables
which could be used and used to create more effective journeys over
there with pre-existing data that we have. So that's pretty much
everything, thank you so much and just in case if you have any other
questions my name is Purusottam Singh, you can reach out to me, thank
you.
