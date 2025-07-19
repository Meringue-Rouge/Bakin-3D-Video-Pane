# Bakin-3D-Video-Pane
ビデオファイルをインポートし、RPG Developer Bakinのイベントに変換します。 3Dビデオ・エンティティとして使用できます。
Imports a video file and converts it into an event in RPG Developer Bakin. It can be used as a 3D video entity.

<img width="300" height="400" alt="image" src="https://github.com/user-attachments/assets/f807f3d5-dd10-4e13-95ee-277e52c1ec15" />


> [!CAUTION]
> これはBakinで動画ファイルを再生するのではなく、一連の画像を再生します。
> 長い動画、高フレームレート、高解像度は、Bakinでメモリを大量に消費します。
> 160x90の解像度で9分のビデオを15fpsで撮影すると、ひどいラグが発生する。 短い動画であれば問題なく動作しますが、一度に多くの異なる動画を読み込まない方がいいでしょう。
> 
> This doesn't play a video file in Bakin, but rather, plays a series of images.
> Long videos, high framerates or high resolution, will use a load of memory in Bakin.
> A 9 minute video at 160x90 resolution at 15 fps takes causes severe lag. For short videos it works fine, but it's best to not have too many different ones loaded at once.

## 使用方法
- ZIPを解凍し、リリースページからEXEファイルを実行してください。
- 動画ファイルを選択します。
- フレームレートを決める：フレームレートを滑らかにすると、動画によってはスプライトの量が大幅に増えるので、長い動画は避け、フレームレートを上げすぎないようにします。
- 画面サイズを決める：小さければ小さいほど解像度は下がりますが、パフォーマンスやファイルサイズは良くなります。 大きくすると、より多くのアニメーションを作成する必要があるので、注意してください。
- エクスポート：RPG Developer BakinイベントTXTを含む必要なファイルをすべて作成します。
- frame_interval.txtファイルを開き、フレーム間隔の値をコピーします。
  - 小数がある場合は、完全に同期した動画にならず、Bakinがフィールドで小数を受け付けないため、理想的ではありません。
- RPG Developer Bakinで、2Dスプライトをドラッグ＆ドロップする要領で、part001（first_frameではない）を3Dワールドにドラッグ＆ドロップして素早くインポートします。
- 画像のサイズをエクスポートした画像サイズに設定します。
- 表示時間をframe_interval.txtのフレーム間隔の値に設定します。
- アニメーションの再生ループをloopかnoneに設定します。
- OKを押してインポートします。
- オブジェクトがマップに表示されたら、それをイベントにします。
- eveht txtファイルをインポートします。
- 空のイベントシートを削除します。
- イベントのモデルを、新しく追加したビデオの2D Castに設定します。 first_frameから始まるのが理想的です。
- 最後に、オーディオを追加したい場合は、エクスポートしたオーディオファイルをインポートし、サウンドエフェクト（SE）として設定し、イベントの一番最初に再生します。


## Usage (English)
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
- Siluman for the idea of making 3D videos working.
- Grok for the coding AI.
