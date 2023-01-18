# ChatCLI - COMP3331 Computer Networks & Applications Assignment

## Contents

[[_TOC_]]

## 0. Change Log
- Version 1.0 released on 5th October 2021.
- Version 2.0 released on 18th October 2021: when a user timeouts, the notification that the user has logged out should be sent to all other users.

## 1. Goal and learning objectives

Instant messaging applications such as WhatsApp, WeChat, Telegram, Signal, etc. are widely used with millions of subscribers participating in them globally. In this assignment, you will have the opportunity to implement your own version of an instant messaging application. In addition to basic messaging functionality, you will also implement many additional services that are available in many of the aforementioned applications. Your application is based on a client server model consisting of one server and multiple messaging clients. The server is mainly used to authenticate the clients and direct the messages (online or offline) between clients. Besides, the server also has to support certain additional functions (presence notification, blacklisting, timeout, etc.). You should also implement functionality that allows clients to send peer-to-peer messages to each other that bypasses the server.

### 1.1 Learning Objectives

On completing this assignment, you will gain sufficient expertise in the following skills:
- Detailed understanding of how instant messaging services work.
- Expertise in socket programming.
- Insights into designing an application layer protocol.

## 2. Assignment Specification

The assignment includes 2 major modules, the server program, and the client program. The server program will be run first followed by multiple instances of the client program (Each instance supports one client). They will be run from different terminals on the same machine (so you can use `localhost`, i.e., `127.0.0.1` as the IP address for the server and client in your program). All interaction with the clients will be through a command line interface.

### 2.1 Server

- User Authentication
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
The client should provide a login prompt to enable the user to authenticate with the server. The authentication process was discussed in detail earlier.

#### Message
The client should allow the user to send a message to any other user and display messages sent by other users. The client should also allow the user to send a broadcast message to all online users. The message may contain uppercase characters (A-Z), lowercase characters (a-z), digits (0-9), special characters (~!@#$%^&*_-+=`|\(){}[]:;"'<>,.?/) and white spaces. During marking we will use short messages that are a few words long.

#### Notifications
The client should display presence notifications sent by the server about users logging in and out from the server.

#### Find users online
The client should provide a way for the user to obtain a list of all the users currently online from the server.

#### Find online history
The client should provide a way for the user to obtain a list of all users who had logged in within a user specified time period.

#### Blacklist
The client should allow a user to block a user from sending any further messages, receive presence notifications or check if they are currently online or were online in the past. The client should also allow a user to unblock a user that was earlier blocked.

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
<td>Send [message] to [user] through the server. If the user is online then deliver the message immediately, else store the message for offline delivery. If [user] has blocked Yoda, then a message to that effect should be displayed for Yoda. If the [user] is invalid or is self (Yoda) then an appropriate error message should be displayed. The [message] used in our tests will be a few words at most.
</td>
</tr>
<tr>
<td>

`broadcast [message]`

</td>
<td>Send [message] to all online users except Yoda and those users who have blocked Yoda. Inform Yoda that message could not be sent to some recipients.
</td>
</tr>
<tr>
<td>

`whoelse`

</td>
<td>This should display the names of all users that are currently online excluding Yoda and any users who may have blocked Yoda. Users can be displayed in any order.
</td>
</tr>
<tr>
<td>

`whoelsesince [time]`

</td>
<td>This should display the names of all users who were logged in at any time within the past [time] seconds excluding Yoda and any users who may have currently blocked Yoda. Note that this, may include users that may currently be offline. If [time] is greater than the time since when the server has been running, then all users who logged in since the sever initiation time should be listed. This suggests that you will need to keep a login history since the start of the server. Users can be displayed in any order.
</td>
</tr>
<tr>
<td>

`block [user]`

</td>
<td>blocks the [user] from sending messages to Yoda, receive presence notifications about Yoda and be able to check if Yoda is currently online or Yoda’s online history. A message should be displayed to Yoda confirming the blocking action. [user] must not be informed that Yoda has blocked them. If [user] is self (i.e., Yoda) or invalid, then an appropriate error message should be displayed. It is not necessary that [user] is currently online. One user may block multiple other users.
</td>
</tr>
<tr>
<td>

`unblock [user]`

</td>
<td>unblocks the [user] who has been previously blocked by Yoda and reverse all the actions manifested by the previous block command. A message should be displayed to Yoda confirming the unblocking action. If [user] is self (i.e., Yoda) or is invalid or was not previously blocked, then an appropriate error message should be displayed. It is not necessary that [user] is currently online.
</td>
</tr>
<tr>
<td>

`logout`

</td>
<td>log out user Yoda.
</td>
</tr>
<tr>
<td>

`startprivate [user]`

</td>
<td>This command indicates that user Yoda wishes to commence p2p messaging with [user]. The server should first ask [user] if they are willing to engage in a private chat with Yoda. If [user] declines, then the server should inform Yoda accordingly. If [user] agrees, then Yoda’s client should obtain certain information about [user]’s client from the server. If [user] has blocked Yoda, then the server need not query [user] and an appropriate error message should be displayed to Yoda. If [user] is offline, invalid, or self then appropriate error messages should be displayed to Yoda. If the private chat session can proceed, Yoda’s client should establish a TCP connection with [user]’s client. A confirmation message should be displayed to Yoda. This TCP connection should remain active till the private chat is stopped or one the user logs off.
</td>
</tr>
<tr>
<td>

`private [user] [message]`

</td>
<td>Send [message] to [user] directly without routing through the server. If the user is no longer online at the port obtained via the previous command, then a message to that effect should be displayed to Yoda. If Yoda has not executed startprivate before this command, then an appropriate error message should be displayed. Note that, Yoda may execute startprivate [user] before [user] blocks Yoda. In this instance, Yoda can still use this command to send a message to [user]. Other error messages (e.g. offline, invalid, etc.) are consistent with those indicated in the above command.
</td>
</tr>
<tr>
<td>

`stopprivate [user]`

</td>
<td>This command indicates that user Yoda wishes to discontinue the p2p messaging session with [user]. Either user can issue this command (i.e., it doesn’t have to be the one who initiated the private chat). A message to this effect should be displayed on the terminal for [user]. The TCP connection established between the two end points should be closed. An appropriate error message should be displayed to Yoda if there does not exist an active p2p messaging session with [user] (i.e, startprivate was not executed with this [user]).
</td>
</tr>

</table>
