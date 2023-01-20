# ChatCLI

## 0. Background

Instant messaging applications such as WhatsApp, WeChat, Telegram, Signal, etc. are widely used with millions of subscribers participating in them globally. This is an assignment of COMP3331 Computer Networks & Applications.

## 1. Goal and learning objectives

On completing this assignment, I have gained sufficient expertise in the following skills:
- Detailed understanding of how instant messaging services work.
- Expertise in socket programming in Python 3.
- Insights into designing an Application Layer Protocol.

## 2. Design Specification

### 2.1 Server

#### User Authentication
A credentials file credentials.txt is used as the database of users' credential. Upon execution, a client will first set up a TCP connection with the server. The client will then prompt the user to enter the username and password.
- If the username and password matches an entry in credentials.txt, the client can use the app.  
- If the username does not exist, it is assumed that the user is creating a new account and the sever sends an appropriate message to the client. The client prompts the user to enter a new password. The password is sent to the server. The server creates a new username and password entry and allows the new user to use the app.
- If a user failed 3 consecutive attempts for the account authentication, this user will be blocked for a duration of block_duration seconds. The client prompt for this user will also be terminated.

#### Timeout
The server supports automatically logging out inactive clients.

#### Presence Broadcasts
The server supports notifying the presence/absence of other client logged into the server.

#### List of online client
The server supports client to query about all the other online clients.

#### Online history
The sever supports client to query about the clients who were online within a specified time period.

#### Message Forwarding
The server supports forwarding each instant message to the correct recipient when they are online.

#### Offline Messaging
The server supports storing each offline message to the correct recipients when they are offline.
The server supports sending stored offline messages once the recipients are back online.

#### Message Broadcast
The server supports clients to broadcast messages to all online clients. Offline messaging is not required for broadcast messages.

#### Blacklisting
The server supports clients to block / unblock any other user.

### 2.2 Client

#### Authentication
The client must log in to complete the authentication with the server.

#### Message
The client allows users to send messages to other users and to receive messages sent by other users. The client also allows users to broadcast messages to all online users.

#### Notifications
The client allows users to receive notifications of other users' online status from the server.

#### Find users online
The client allows users to query the server about all the online users.

#### Find online history
The client allows users to query the server about the users who were online within a specified time period.

#### Blacklist
The client allows users to block other users from sending messages, receiving presence notifications and querying current online status or in a specified time period. The client also allows users to unblock a blocked user.

#### P2P messaging
The client allows users to send direct messages without being routed via the server to each other.

### 2.3 Commands supported by the client

<table>
<tr>
<th>Command</th>
<th>Description</th>
</tr>
<tr>
<td>

`message [user] [message]`

</td>
<td>
Send [message] to [user] via server.
<ul>
<li>If [user] is online then send [message] immediately, else send [message] when [user] is online.</li>
<li>If [user] has blocked the sender, [user] will not receive [message].</li>
<li>If [user] is invalid or is the sender, an error message will be displayed to the sender.</li>
</ul>
</td>
</tr>
<tr>
<td>

`broadcast [message]`

</td>
<td>Send [message] to all the other online users who have not blocked the sender. The sender will be notified with the unsuccessful recipients.
</td>
</tr>
<tr>
<td>

`whoelse`

</td>
<td>Display all the other online users who have not blocked the user.
</td>
</tr>
<tr>
<td>

`whoelsesince [time]`

</td>
<td>
Display all the other users who were online at any time within the past [time] seconds.
<ul>
<li>It may include the users who have currently blocked the user.</li>
<li>It may include the users who are currently offline.</li>
<li>If [time] is greater than the duration of the running server, all users who logged in since the start of the sever should be displayed.</li>
</ul>
</td>
</tr>
<tr>
<td>

`block [user]`

</td>
<td>
Block [user] from sending messages to the user, receiving presence notifications of the user and querying the user's current online status or in a specified time period.
<ul>
<li>A confirmation message will be displayed once the blocking is in action.</li>
<li>[user] will not be informed of being blocked.</li>
<li>An error message will be displayed when [user] is invalid, already blocked or [user] is the user.</li>
</ul>
</td>
</tr>
<tr>
<td>

`unblock [user]`

</td>
<td>
Unblock blocked [user].
<ul>
<li>A confirmation message will be displayed once the unblocking is in action.</li>
<li>[user] will not be informed of being unblocked.</li>
<li>An error message will be displayed when [user] is invalid, is not blocked or is the user.</li>
</ul>
</td>
</tr>
<tr>
<td>

`logout`

</td>
<td>Log out the user.
</td>
</tr>
<tr>
<td>

`startprivate [user]`

</td>
<td>
[user] will be prompted a P2P messaging request sent by the user.
<ul>
<li>A TCP connection will be established along with a confirmation message displayed if [user] accepts the request.</li>
<li>A response message will be displayed if [user] declines the request.</li>
<li>An error message will be displayed if [user] is invalid, offline or the user itself, or has blocked the user.</li>
<li>The TCP connection will remain active till the p2p session is stopped or either user goes offline.</li>
</ul>
</td>
</tr>
<tr>
<td>

`private [user] [message]`

</td>
<td>Send [message] to [user] directly without routing via server.
<ul>
<li>If [user] is no longer online at the port obtained via the previous command, a message to that effect will be displayed.</li> 
<li>An error message will be displayed if there is no TCP connection established with [user].</li>
<li>Other error messages (e.g. offline, invalid, etc.) are consistent with those indicated in the above command.</li>
</ul>
</td>
</tr>
<tr>
<td>

`stopprivate [user]`

</td>
<td>
Terminate the P2P messaging session with [user]. Either user can use this command. 
<ul>
<li>[user] will be prompted a message first and then the TCP connection will be terminated.</li>
<li>An error message will be displayed if [user] is invalid, offline or the user itself, or is not on a p2p session with the user.</li>
</ul>
</td>
</tr>

</table>
