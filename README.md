# bbs5: BBS/CMS/MOO Hybrid
# License: [http://www.gnu.org/licenses/agpl-3.0.en.html]
# Author: Mario McGinley

Generic Asyncio/aiohttp based programmable web system.
Internals are exposed to frontend as programmable components.
Current Stack: Asyncio/Aiohttp/Goblin/OrientDB In-Memory Redis/RabbitMQ alternative/OrientDB/Tinkerpop Rexster/Elastic Search

Jinja2 memory templates are extended to pull from OrientDB.
Goblin Query Data is sent over the RPC bridge to the PyPy Sandbox then reconstructed inside the sandbox internally and overrides the DB Object .save() method to talk back to the outer Goblin library through a JSON Message Object.  The result is an internally held Goblin object list inside the sandbox that saves back to the ACL partitioned outer Goblin library.  This sandboxes both Python code execution and the database to the ACL.
Web Objects are programmable objects similar to a MOO or ZOPE.
Programmable Command Line Parser (from MOOP).
Objects are held in a Folder/File tree hierarchy then folders objects may be collected and rendered with a custom collector object.




## Stock Objects / <div> Types:
* -WebRTC Video-to-Video for user-to-user chat
* -One-To-Many Video Streamer for Sysop to World (pubnub API or custom)
* -Sharefest style bandwidth reduction of media assets
* -Sysop Video WebRTC Contact Form
* -User Video WebRTC Contact Form
* -Wiki
* -Algorithmic Art helper Library
* -Music Tracker
* -Misc. Demo Effects
* -Poll
* -Message Board
* -HTML Stream (HTML Scrolling Log)
* -ANSI Art (Pixi*js Renderer)
* -Vector Art (?)
* -3d Web Design: GLAM (https://tparisi.github.io/glam/#about)
* -Door Games: Diplomacy (https://en.wikipedia.org/wiki/Diplomacy_(game))
