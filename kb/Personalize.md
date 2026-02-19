# Personalize

## Profile & Database Management

## Events Timeline Analysis

## List & Segment Management

## Custom Profile Properties

Hi there. This is a quick demo of Gupshop\'s Personalize module. So
whenever we want to navigate to our customer data, we can click on
Personalize, and there are three, in fact, four tabs. In the Guide
section, you can get a quick access to the official documentations,
wherein the document can help you guide on how to create lists,
segments, how to create new profile properties, and what is the overall
use of profiles. In the All Profile section, you can have a bird\'s eye
view of your complete database. You can have a look on your profiles.
You can also have a look on the total number of profiles, how many are
active on a monthly basis, and what is the total number of mobile
numbers available. Similar information in a graphical manner, and a few
shortcuts of other modules that are present. So you can access Campaign
Manager, you can access Bot Studio, you can access Integrations, and
also click to WhatsApp ads. And again, a list of all the users that are
currently there on the console. So if at all I click on any one of these
users, for example, I can get two types of information. Number one, I
can get their information or also see what lists and segments are they a
part of. I can also see their profile properties as well. I can quickly
update it, delete it, or in fact, add new information as well. Some
system-generated information, wherein when was this profile created,
when was it last active, and all of that, and all the console events
that will be present on the right-hand side. So this is the Events
Timeline, wherein you can see all the events that the person is
performing. So let\'s say if they have received a campaign, you will be
able to see that event. You can see whether the message was delivered to
them or not, whether did they read it or not, if at all the user\'s read
events are on. You can also see if at all they clicked on any button or
not. In fact, you can also see if at all there is any third-party
integration through which any events are coming from any external system
like CleverTap, MoEngage, or even the website directly. You can also
have a bird\'s eye view of those events as well. So events like sign-up,
product purchase, page browse, page load, and all of those events can
also become a part of this Events Timeline. The second tab is Lists and
Segments, wherein you can do two things. Either you can import and
export data onto the Gupshup console by simply clicking on \"Create a
new list\". Give it some name, create. You can also download a sample
file to match the format. And if at all you have the file ready in the
required format, you can simply browse it and simply select it. Click on
\"Save,\" and then the list will get updated in a few minutes with all
the data in the list. The second thing is segment creation, which is
basically used for targeted marketing. So there are two options in the
toast message: \"Create static segment,\" which does not update by
itself, or you can also create a \"Dynamic segment,\" which can update
on a daily basis. So if at all I click on \"Dynamic segment,\" I can
click on \"Next\". I can give it a name, and then in the definition, I
can start defining the criteria which needs to be a part of the segment.
So there are two logics: either it can be \"Properties about someone,\"
wherein you can filter out on the basis of a person\'s profile property.
So you can simply select, let\'s say in this case, I select \"Gender\"
should be equal to or should contain (there are several values over
here: \"contains,\" \"does not contain,\" \"ends with,\" \"starts
with\"). So in this case, I\'ll say \"equal to,\" and then I can enter
the value; let\'s say I say \"Male\". I can also add \"and\" or \"or\"
conditions and simply choose another property. Let\'s say in this case,
I select \"City\" equals to \"Delhi\". Then I can click on \"Preview
segment\" and then I can create a segment, and then this segment can be
used for campaigning. It can be used to run automated campaigns,
basically send out different kinds of messages which can be targeted
towards their activities. The second type of filtration can be done on
the basis of \"What someone has done or not done,\" which is basically
events. So you can simply select the source. The source can again be on
the basis of a custom integration, wherein third-party events are coming
from an external source, which could be a website or any other tool like
CleverTap or MoEngage, or any system could be an app as well, or they
can also be on the basis of WhatsApp events. So in this case, if at all
I select \"WhatsApp,\" I can now see and I can create a segment of all
the people who might have read or not read a given campaign. So let\'s
say we are trying to get a list of all the users who read a campaign,
who read a recent campaign that we deployed. So you can simply say
\"Count of messages read at least once\" overall time. It can also be on
the basis of dates as well. In this case, I\'ll say \"Overall time,\"
and I can also add a filter, wherein I can filter it on the basis of
\"Campaign ID,\" and then you can simply enter the Campaign ID which was
used in the broadcasting so that the filtration can be done on the basis
of that Campaign ID. Secondly, it can also be done on the basis of
third-party events, as I mentioned before. So I can select a custom
integration, I can select an event. Then I can select the frequency,
overall time, and then I can preview segment and then create a segment.
The third tab is Profile Properties, wherein you can see all the profile
properties that are there on the console. There are two types: primary
and custom. Primary are all the system profiles that are always there by
default. And the custom profiles are the ones that a user creates by
themselves to capture additional information. You can always add a new
property like this. Give it some kind of a name; in this case, let\'s
say let\'s call it a \"Sign-up Date\". And then you can select the data
type. In this case, it\'s going to be \"Date,\" and you can simply click
on \"Save\". And the profile gets created. And now, every time you
upload a list, and in the list, the sign-up date has a value, that value
will get mapped against the sign-up date of the person\'s profile. So
this is a quick overview of Personalize and how to use Personalize in
bots. Here\'s a small example for a demo journey, wherein you can
trigger a bot by saying this particular keyword. You can ask somebody
these types of questions. The response momentarily needs to be stored in
a variable. These are all string variables. And then you can call that
variable in the Personalized node by simply selecting that specific
property and calling that value of the variable in the value section. So
as soon as a person starts this journey and then they start answering
these questions, all these values, the responses, will get mapped
against their personalized profile properties. So this is how you use
Gupshup\'s Personalized module to capture and populate more and more
customer data and then segment it, and then which can be used for
targeted marketing.
