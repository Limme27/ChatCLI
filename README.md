# ChatCLI - COMP3331 Computer Networks & Applications Assignment

## 1. Goal and learning objectives

Instant messaging applications such as WhatsApp, WeChat, Telegram, Signal, etc. are widely used with millions of subscribers participating in them globally. 

### 1.1 Learning Objectives

On completing this assignment, I gain sufficient expertise in the following skills:
- Detailed understanding of how instant messaging services work.
- Expertise in socket programming.
- Insights into designing an application layer protocol.

## 2. Design Specification

### 2.1 Server

#### User Authentication
You may assume that a credentials file called credentials.txt will be available in the current working directory of the server with the correct access permissions set (read and write). This file is NOT available at the client. The file will contain username and passwords of authorised users. They contain uppercase characters (A-Z), lowercase characters (a-z), digits (0-9) and special characters (~!@#$%^&*_-+=`|\(){}[]:;"'<>,.?/). An example credentials.txt file is provided on the assignment page. We will use a different file for testing so DO NOT hardcode this information in your program. You may assume that each username and password will be on a separate line and that there will be one white space separating the two. There will only be one password per username. There will be no empty lines in this file.

Upon execution, a client should first setup a TCP connection with the server. Assuming the connection is successful, the client should prompt the user to enter a username. The username should be sent to the server. The server should check the credentials file (credentials.txt) for a match. If the username exists, the server sends a confirmation message to the client. The client prompts the user to enter a password. The password is sent to the server, which checks for a match with the stored password for this user. The server sends a confirmation if the password matches or an error message in the event of a mismatch. An appropriate message (welcome or error) is displayed to the user. In case of a mismatch, the client is asked to enter the password again (see discussion on blocking later). If the username does not exist, it is assumed that the user is creating a new account and the sever sends an appropriate message to the client. The client prompts the user to enter a new password. You may assume the password format is as explained above (no need to check). The password is sent to the server. The server creates a new username and password entry in the credentials file (appending it as the last entry). A confirmation is sent to the client. The client displays an appropriate welcome message to the user. You should make sure that write permissions are enabled for the credentials.txt file (type “chmod +w credentials.txt” at a terminal in the current working directory of the server). After successful authentication, the client is considered as logged in (i.e., online).

When your assignment is tested with multiple concurrent clients, the server should also check that a new client that is authenticating with the server does not attempt to login with a username that is already being used by another active client (i.e., a username cannot be used concurrently by two clients). The server should keep track of all active users and check that the username provided by an authenticating client does not match with those in this list. If a match is found, then a message to this effect should be sent to the client and displayed at the prompt for the user and they should be prompted to enter a username.

As noted above, on entering an invalid password, the user is prompted to retry. After 3 consecutive failed attempts for a particular username, this user is blocked for a duration of block_duration seconds (block_duration is a command line argument supplied to the server) and cannot login during this duration. The client should quit in this instance.

#### Timeout
The server should check that all logged on users are active. If the server detects that the user has not issued any valid command for interacting with the server or for peer-to-peer messaging for a period of timeout seconds (timeout is a command line argument supplied to the server), then the server should automatically log this user out. The receipt of a message or typing an invalid command does not count.

#### Presence Broadcasts
The server should notify the presence/absence of other users logged into the server, i.e., send a broadcast notification to all online users when a user logs in and logs out. Note that, when a user is logged off due to timeout, a broadcast notification is sent to all online users.

#### List of online users
The server should provide a list of users that are currently online in response to such a query from a user.

#### Online history
The sever should provide a list of users that logged in for a user specified time in the past (e.g., users who logged in within the past 15 minutes).

#### Message Forwarding
The server should forward each instant message to the correct recipient assuming they are online.

#### Offline Messaging
When the recipient of a message is not logged in (i.e. is offline), the message will be saved by the server. When the recipient logs in next, the server will send all the unread messages stored for that user (timestamps are not required).

#### Message Broadcast
The server should allow a user to broadcast a message to all online users. Offline messaging is not required for broadcast messages.

#### Blacklisting
The server should allow a user to block / unblock any other user. For example, if user A has blocked user B, B can no longer send messages to A i.e. the server should intercept such messages and inform B that the message cannot be forwarded. Blocked users also do not get presence notifications i.e., B will not be informed each time A logs in or logs out. Blocked users are also unable to check the online status of the user blocking them, i.e., B will not be able to see if A is online currently or in the past (i.e., online history).

### 2.2 Client

#### Authentication
The client must log in to complete the authentication with the server.

#### Message
The client supports users to send messages to other users and to receive messages sent by other users. The client also supports users to broadcast messages to all online users.

#### Notifications
The client supports users to receive notifications of other users' online status from the server.

#### Find users online
The client supports users to query the server about all the online users.

#### Find online history
The client supports users to query the server about the users who were online within a specified time period.

#### Blacklist
The client supports users to block other users from sending messages, receiving presence notifications and querying current online status or in a specified time period. The client also supports users to unblock a blocked user.

#### P2P messaging
The client supports users to send direct messages without being routed via the server to each other.

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
