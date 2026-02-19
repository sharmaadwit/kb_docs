# Flows

## WhatsApp Flows Overview

## Using the Flow Builder

## Designing Terminal Journeys

Hi everyone. My name is Purushottam. People also know me as Puru, part
of the pre-sales team. I, along with, lead the India-based pre-sales
team. Right. So, in this video I\'m going to talk about WhatsApp Flows.
I\'m sure most of you will have certain ideas about what a WhatsApp flow
is. But to start off with, I would want to want you to look at a
particular video which I mean, which is nothing but a WhatsApp flow, and
then after we\'ll get into the platform in order to learn how do you
build it, how do you deploy it, and how the platform works around it.
Right? o, yeah. This is a campaign which Policybazaar was doing with us.
Basically, Policybazaar, all of you will know, it\'s an insurance
broker. So, this video is nothing but a video demonstration of how
Policybazaar used WhatsApp flows to go ahead and generate more more
leads, get in the onboarding details from the end users altogether. So,
this this video which you see, the very first thing which starts off
here is the template. So, basically Policybazaar sent out a particular
template to the end user, saying that, \"Hey, you\'re interested, would
if you would be interested in buying so-and-so term life insurance\". If
the user clicks \"Proceed,\" this is the form which opens up. This form
is nothing but WhatsApp Flows. It\'s a feature wherein dynamic elements
such as a date picker, a free text, a button, or a drop-down button,
radio buttons, all of those things which you normally see on a mobile
application or a website form fill up, all of those things can happen
within the WhatsApp universe, within the WhatsApp page. You look at it
wherein it\'s a web view opening up within the WhatsApp screen. That\'s
what a WhatsApp flow is, wherein if if we need to ask the user a lot of
questions which is not possible using a traditional step-by-step flow,
then WhatsApp flows comes in really handy, wherein you could ask those
same questions in a form format, wherein they could fill out the details
easily, just to go ahead and have a better user experience altogether.
Yeah. So, that\'s now that we have defined a WhatsApp flow, what it is,
and I\'ve shown you how does it function exactly, let me quickly go
ahead and show you how do you build it on our platform. So, the very
first thing which you do is you come here to Bot Studio. There is a
separate section for WhatsApp flows. As soon as you come here, all of
the line items which you see are nothing but individual WhatsApp flows.
Let me take an example of this one here, which is DBS. This is a lead
generation journey which we built for them in order for them to go ahead
and qualify and onboard customers who want to open savings bank account
over there. Okay. So, it\'s pretty simple as you see. There is this
starting node which asks for a flow ID, and there is this terminal node
which defines what happens after the WhatsApp flow is completed. Now,
this flow ID is nothing but this encapsulates the entire WhatsApp form
that we have created. Right? So, to create a form up till now, it is not
available out of the box on the console platform. We\'ll have to go to
the solutions mode platform, or even we could build it using the Meta
Developer Platform over there. So, quickly let me take you to the
playground here. Over here, this is the Meta Developer Platform wherein
you could build your WhatsApp flows. So, as you could see, there is this
one screen. You could I mean, as you could see, there is this one screen
which covers all of these details, asking the user. You can edit it. I
mean, maybe if you want to change the details here, that\'s fine. You
can enter whatever you want, and that would reflect in your render in
real time over here for you to go ahead and define different WhatsApp
flows. So, the options which it gives are in four different categories.
One is text that you could render. The second is media, of course,
images. Text answers, as in if you need answers to particular questions.
And then after, there is selections, as in you can have single choice,
multiple choice questions which you could ask, or even give the user a
drop-down menu or an opt-in approach as in a toggle button over there.
Okay. These are the elements. Once you have created everything, you get
this \"Copy Flow JSON\". Let me quickly open up a new notepad for this
and show you. So, once you have created the UI, you have to get this
JSON file. Okay, JSON file, which is nothing but which actually maps out
the entire journey that you have built, and you have to take it to
WhatsApp Flow Builder. This is our own product, wherein you have to I
mean, you can create a new flow here, and then after select details such
as what Waba number do you want to configure it to and what\'s the name.
So, let me just go ahead and \"Testing Flows and Puru\". I\'m giving it
a unique name here. Category, you can select any which one of these. It
actually doesn\'t matter, to be very honest with you. Yeah. So, then
after you select whether you want it static or dynamic. Let me define
what is a static flow. A static flow is a predefined form that you give
out to the end users, no matter what. But a dynamic flow is basis each
selection in that particular form or WhatsApp flow, when you move on to
the next page of that particular flow, then it changes according to the
behavior or according to the inputs which have come in. Just keep it
simple and give you a fair idea. I\'m going to keep it static. You can
go ahead and select these things here. I\'ll select \"Self-Serve
India\". Account type. And then you go on to submit that. Post that you
get the option to go ahead and paste your JSON file which you have
copied from here in the playground. You can obviously build it right
here as well in in this section if you want to. But I\'ve I\'ve created
this flow. It has this flow ID, if you could see. And I\'ll go ahead and
edit this and put in my JSON file right here. Sorry, I I think I didn\'t
copy that properly. Copy it. Put it here. Put the JSON file here. You
have the flow builder right here as well. You can go ahead and add
screens just like the playground over there, screen name, everything.
But I find the Meta platform pretty easy and more UI friendly in order
to build this. Hence, I copy the JSON from there and put it here. You
can save it as drafted and then get to preview the journey if you have
to. And yeah, you can go ahead and check the preview. It\'ll load out
load up something like this. The same thing which we have built over
there. There are different pages if you could see, just like what I have
built over there. Over here, if you could see, then there are two
different pages that we have built. One is the feedback one, one by two
and two by two. Same thing rendered over there if you see. So,
similarly, I mean, you build your journey right here on the Meta
Developer Platform, copy the JSON, put it here, check that for preview.
It is necessary that you check that for preview because there at times
it does fail. And then you publish. Once you have published, as I was
saying, you get this flow ID. This ID you have to copy it from here.
Move it. Move back to Console, go to WhatsApp Flows, and create a new
flow and put that ID over there. Once you have done so, I\'ll go back to
the same example. Once you have done so, your WhatsApp flow is ready.
Okay. But you need to do one extra thing before you complete this. After
filling out the starting node, you also have to use this terminal node
and define a journey over here. What is that? We\'ll look at in detail.
But before that, let\'s go back to the journey builder and show you how
to connect this WhatsApp flow which we have built into a real journey.
So, DBS. I\'ll just go to the same. Yeah, DBS Lead Generation Journey.
So, it\'s pretty much like a simple journey that we create on Journey
Builder. Starts with a starting node which defines the input which will
trigger this journey, that is \"DBS Guru\". This is the keyword I\'ve
kept to trigger this particular journey. And then we I have this welcome
image. If you want it, keep it there. If you don\'t want it, just get it
over with. No problems. Then there is this message which I have defined.
See, until here it is just a normal journey, normal two-way
conversational journey which we use the Journey Builder to build it. But
post that, you use this block which is this one here: WhatsApp flow. You
drag and drop that, connect it to whichever journey you want to. And
then after you go ahead and select from the drop-down of all of the
WhatsApp flows which is available. This drop-down gets populated by the
list of options which you have given here, WhatsApp flows, the one which
we defined just right now, right? With the flow ID we defined a WhatsApp
flow. So, you need to go ahead and select one of those and whatever
journey you have created, and you\'re good to go. That\'s that\'s all
you have to do to go ahead and connect a WhatsApp flow to a particular
journey in the Journey Builder. And once you have done that, of course,
now I\'m going to go ahead and talk about the terminal journey, as in
what I showed you there. So, let me just type \"DBS\" again. \"DBS
Terminal Journey.\" What happens here? This is nothing but after the
WhatsApp form, which was here. Let me show you this. Yeah. Let me go
back a little bit. So, this is a form which is getting continued, right?
It started here. If I go back a little bit, so let\'s imagine that,
okay, let\'s imagine that this piece until this piece, this message
which has come up, \"Hey, welcome to Policybazaar\", this is part of our
journey, which is nothing but this one, DBS Lead Gen. Let\'s imagine
that these steps, these steps, these three, the welcome image, the
message, all of this is part of the this is what is here. Okay? This
message which comes up post that, once this node is triggered, WhatsApp
flow, the WhatsApp flow journey triggers over here, if you see. Yeah.
This form popping up, this is built inside this node here. And once this
form is filled up to whatever pages it has, doesn\'t matter. Once that
is done and the form closes, then comes the terminal journey in action.
Okay. Yeah. So, now the form has closed and it has come back to a real
journey. I mean, as in, that is also real as in, what I\'m trying to say
is a step-by-step journey. Here if you see, coming back, yeah. It has a
link and it is taking the user to an external website. But point is, as
soon as the WhatsApp flow, this one, this form closes up, this message
is part of the external journey, as in terminal journey. And that\'s
what we have defined in here, if you go if you see this, uh DBS Terminal
Journey. Yeah. So, that is after the form closes, I\'m asking for OTP.
I\'m showing the images over there and the journey follows up. But now
we need to go ahead and connect this terminal journey to WhatsApp flow.
So, in the WhatsApp flow journey builder again, if I show you this, if
you see this clearly, you\'ve got terminal journey here. Right? That\'s
it. That\'s how you build a WhatsApp flow, build, link it to a journey,
and then after deploy it on a production environment. Thanks a lot.
