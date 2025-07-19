# Bakin-3D-Video-Pane
Import a video file and convert it into an event and image atlases to be used as a video that can be placed in 3D space in RPG Developer Bakin.

## Usage
- Extract the ZIP and run the EXE file from the releases page.
- Select a video file.
- Define the frame rate: smoother frame rates increase the amount of sprites significantly, depending on video, so avoid long videos and don't go overboard on the frame rate.
- Define the screen size: the smaller, the lower the resolution, but the better the performance / file size. The bigger, the more animations need to be created, so be careful.
- Export: this creates all the necessary files, including an RPG Developer Bakin event TXT that already handles timings between different parts of the video.
- Open the file frame_interval.txt and copy the value of the frame interval.
  - If there are decimals it isn't ideal as it won't be a perfectly synced video and Bakin doesn't accept decimals in the field.
- In RPG Developer Bakin, drag and drop part001 (not first_frame) into the 3D world, just like you're dragging and dropping a 2D sprite to quickly import it.
- Set the size of the image to the image size you've exported at.
- Set the Display Time to the value of frame interval in frame_interval.txt
- Set the animation playback loop to either loop or none.
- Press OK to import.
- When the object appears in the map, make it an event.
- Import the eveht txt file.
- Delete the empty event sheet.
- Set the event's model to the 2D Cast of your newly added video. Ideally it should start at first_frame.
- Finally, if you want to add the audio back; import the audio file that it exported, set it as a Sound Effect (SE), and then play it at the very start of the event.

## Credits
- Siluman for the idea of getting 3D videos working.
- Grok for the coding AI.
