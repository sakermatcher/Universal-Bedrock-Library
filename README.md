# Universal Bedrock Library V 0.1.0 WIP
 - A Bedrock Library to unite universal addon stuff (mainly ingots and ores)
 Most textures are from [Emendatus Enigmatica Java Mod](https://github.com/Ridanisaurus/EmendatusEnigmatica) so if you want to congratulate someone it should be Ridanisaurus which is the most talented minecraft texture maker Ive seen, so go check his work out

 - If anyone wants to chip in ore just suggest something my mailbox is always open on discord and thruought here

## Addon Creator?
 -The target: dont fall into the same problem that modded Java had with having different variations of the same thing. Addon creators out there just have to copy code and textures from this library so that when users download addons they dont have to deal with having to get all the ingot/ores/etc variations for the things that every addon provide. 
 
 -Recomendations: 
 
 - If you are an addon creator please use this library... I also highly recomend taking a look at the set of "[guidelines](#guidelines-total-wiiiip)" that a lot of things have (They explain which items are used for ore processing, which are only for gems, which are only for metals, what every alloy are made of regardless of their crafting process which is up to you, the biomes, dimentions, and y levels of ores, and much more!) that is just to make every material in every addon follow the same guidelines. 
 
 - If you are planning on adding an ingot/ore or something that you think others could have a variation of in their addon that is not on this library I highly recomend for you to use the "universal:..." Identifier so that when users use your addons they'll combine more seamlessly with others 

## Guidelines TOTAL WIIIIP

#### What are these?

Guidelines are obviously not at all mandatory and there is no problem if you decide to use this library without following them, still they are here so that every variation of added items can act in a similar way to the same item added by another creator, in this way making the user have a more seamless experience when switching from one addon to another. The second reason is so that as you will be using the same identifier in your universal items as the rest of the addon creators we dont want that depending on the addon pack that you put on top the behavior for that item changes compleately.

#### 1- universal:

I know you are tired of hearing this but this is the main reason for the pack: using the "universal: ... " identifier for your items/blocks or whatever ONLY in the things that are either on this library or you belive a different addon out there could have a variation of.

#### 2- Common item use

##### Ore processing:

- Just as a disclaimer this is the most optional part because not many addons have an ore processing system, so you can completly skip this and only grab the files that you need.

- If you look at the materials on the library you'll find that there are many items which you probably not know what to use for, let me explain it to you. If in your addon you have an ore processing method (making one raw material turn into 2 ore more ingots/gems instead of having eat only give you one), to unite ore processing across addons Ive the following system in mind, you can make the process be anything, but the items that it yields you will be the same; lets say you wanted to get a gem, then all you'd have to do is smelt its raw form and get 1 gem, but what if you want 2 gems? Then you'll have a procces to convert that raw gem into 2 fragments, which in turn can be smelted to get one gem each, now lets say you'd want to quadruplicate your raw gems, then wad you'd do is passing a raw gem to a process which yields 4 crystals those four crystals each can then go to a process which turns each one into a shard, then another process which turns them to a fragment and finally smelt those 4 fragments to get your 4 gems, and you have just got 4 gems from a single raw! If you want to process metals it would be much like the gems the difference being the names, and in the case of metals they can be quintuplicated. For more info check the processing list below.

###### Gems:

- 1 raw to 4x Crystal
- 1 raw to 3x Shard
- 1 raw to 2x Fragment

###### Metals:

- 1 raw to 5x Chunk
- 1 raw to 4x Pices
- 1 raw to 3x Dirty
- 1 raw to 2x Dust
