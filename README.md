# bbs5: BBS/CMS/MOO Hybrid
# License: [http://www.gnu.org/licenses/agpl-3.0.en.html]
# Author: Mario McGinley

Asyncio/aiohttp based programmable web system.
Jinja2 memory templates are extended to pull from OrientDB.
Bulbflow library is monkeypatched for asyncio asynchronous DB requests to OrientDB over Rexster.
Bulbflow library is monkeypatched for returning the REST Query Data over the RPC bridge to the PyPy Sandbox then the SandboxedBulbs monkeypatched library inside the sandbox reconstructs the REST Query Data internally and overrides the DB Object .save() method to talk back to the outer Bulbflow through a JSON Message Object.  The result is an internally held Bulbs object list inside the sandbox that saves back to the ACL partitioned outer Bulbs library.  This sandboxes both Python code execution and the database to the ACL.
Web Objects are programmable objects similar to a MOO.
uses wcDocker library to render collections of objects in Panels/Windows.
Programmable Command Line Parser (from POO/MOOP).
Objects are held in a Folder/File tree hierarchy then folders objects may be collected and rendered with a custom collector object.
A WebRTC PBX-like exchange is exposed to the outside world for communication with people in a particular BBS.  A global directory of BBS's may index the total online population.  This makes for sort of a distributed cluster of mini-social-network type systems.





## Possible Panel Types:
* -WebRTC Video-to-Video
* -One-To-Many Video Streamer
* -P2P File Sharing
* -Administrator Video WebRTC Contact Form
* -User Video WebRTC Contact Form
* -Wiki
* -Marquee
* -Zoomer
* -Misc Effects
* -Poll
* -Message Board
* -Demo Creation Library
* -AudioPlayer
* -VideoPlayer
* -HTML
* -AdminHTML
* -HTML Stream (HTML Scrolling Log)
* -ANSI Art (Pixi*js Renderer)
* -Vector Art (?)
* -3d Web Design: GLAM (https://tparisi.github.io/glam/#about)
