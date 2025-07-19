import os
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from pathlib import Path
import math
from PIL import Image, ImageTk
import webbrowser


class FrameExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Frame Atlas Extractor")
        self.root.geometry("450x480")
        self.root.resizable(False, False)

        # FFmpeg path
        self.ffmpeg_path = os.path.join(os.path.dirname(__file__), "ffmpeg")

        # Variables
        self.video_path = tk.StringVar()
        self.framerate = tk.StringVar(value="1")
        self.resolution = tk.StringVar(value="160x90")

        # Style
        padding_opts = {'padx': 10, 'pady': 5}

        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Video selection
        ttk.Label(main_frame, text="Select Video File:").pack(anchor="w", **padding_opts)
        ttk.Entry(main_frame, textvariable=self.video_path, width=50).pack(**padding_opts)
        ttk.Button(main_frame, text="Browse", command=self.browse_file).pack(**padding_opts)

        # Framerate
        ttk.Label(main_frame, text="Framerate (fps):").pack(anchor="w", **padding_opts)
        ttk.Entry(main_frame, textvariable=self.framerate, width=10).pack(**padding_opts)
        ttk.Label(main_frame, text="Framerate Preset:").pack(anchor="w", **padding_opts)
        ttk.OptionMenu(main_frame, self.framerate, self.framerate.get(), "0.5", "1", "2", "5", "10").pack(**padding_opts)

        # Resolution
        ttk.Label(main_frame, text="Resolution (widthxheight):").pack(anchor="w", **padding_opts)
        ttk.Entry(main_frame, textvariable=self.resolution, width=10).pack(**padding_opts)
        ttk.Label(main_frame, text="Resolution Preset:").pack(anchor="w", **padding_opts)
        ttk.OptionMenu(main_frame, self.resolution, self.resolution.get(),
                       "160x90", "320x180", "426x240", "640x360", "854x480", "1280x720", "original").pack(**padding_opts)

        # Extract button
        ttk.Button(main_frame, text="Extract Atlas and Audio", command=self.extract_atlas_and_audio).pack(pady=20)


        # Separator
        ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=10)

        # Footer frame
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill="x", side="bottom")

        # Load and scale logo
        logo_path = os.path.join(os.path.dirname(__file__), "software_logo.png")
        try:
            raw_logo = Image.open(logo_path)
            scaled_width = int(self.root.winfo_width() * 0.15) or 67  # Fallback width if winfo_width() returns 1
            aspect_ratio = raw_logo.height / raw_logo.width
            scaled_height = int(scaled_width * aspect_ratio)
            logo_resized = raw_logo.resize((scaled_width, scaled_height), Image.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(logo_resized)
        except Exception as e:
            self.logo_image = None
            print(f"Error loading logo: {e}")

        # Left side: Creator link
        link = ttk.Label(footer_frame, text="Made by Meringue Rouge", foreground="blue", cursor="hand2")
        link.pack(side="left", padx=10)
        link.bind("<Button-1>", lambda e: webbrowser.open_new("https://meringue-rouge.github.io/"))

        # Right side: Clickable logo
        if self.logo_image:
            logo_label = tk.Label(footer_frame, image=self.logo_image, cursor="hand2", borderwidth=0)
            logo_label.pack(side="right", anchor="se", padx=10, pady=5)
            logo_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://meringue-rouge.github.io/"))

        # FFmpeg notice centered
        ttk.Label(main_frame, text="This application uses FFmpeg under the LGPL license.",
                  font=("Arial", 8)).pack(pady=5)


    # Remove show_framerate_presets and show_resolution_presets
    # since we now use OptionMenus


    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv *.mov")])
        if file_path:
            self.video_path.set(file_path)

    def show_framerate_presets(self):
        preset_window = tk.Toplevel(self.root)
        preset_window.title("Framerate Presets")
        preset_window.geometry("150x100")
        presets = ["0.5", "1", "2", "5", "10"]
        for preset in presets:
            tk.Button(preset_window, text=preset, command=lambda p=preset: self.set_framerate(p)).pack(pady=2)

    def show_resolution_presets(self):
        preset_window = tk.Toplevel(self.root)
        preset_window.title("Resolution Presets")
        preset_window.geometry("150x200")
        presets = ["160x90", "320x180", "426x240", "640x360", "854x480", "1280x720", "original"]
        for preset in presets:
            tk.Button(preset_window, text=preset, command=lambda p=preset: self.set_resolution(p)).pack(pady=2)

    def set_framerate(self, value):
        self.framerate.set(value)

    def set_resolution(self, value):
        self.resolution.set(value)

    def get_frame_count(self, video_path, framerate):
        """Get the number of frames based on video duration and framerate."""
        try:
            cmd = [self.ffmpeg_path, "-i", video_path, "-map", "0:v:0", "-c", "copy", "-f", "null", "-"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            duration_line = [line for line in result.stderr.splitlines() if "Duration" in line]
            if duration_line:
                duration_str = duration_line[0].split("Duration: ")[1].split(",")[0]
                h, m, s = map(float, duration_str.split(":"))
                duration = h * 3600 + m * 60 + s
                return max(1, int(duration * float(framerate)))  # Ensure at least 1 frame
            return 1  # Fallback if duration not found
        except (subprocess.CalledProcessError, ValueError):
            return 1

    def calculate_grid(self, frame_count, frame_width, frame_height):
        """Calculate grid size for a single row within 8192x8192 limit."""
        max_size = 8192
        # Maximum columns based on resized frame width
        max_cols = max_size // frame_width
        rows = 1  # Single row atlas

        if max_cols == 0:
            return 1, 1  # Fallback for very large frames

        # Calculate number of atlases needed
        num_atlases = math.ceil(frame_count / max_cols)
        frames_per_atlas = math.ceil(frame_count / num_atlases)

        # Adjust columns to fit frames per atlas
        cols = min(max_cols, frames_per_atlas)

        return cols, rows

    def create_atlas(self, frame_files, output_path, cols, rows, frame_width, frame_height):
        """Create a single-row atlas image from individual frames using Pillow."""
        max_size = 8192
        total_frames = len(frame_files)
        if total_frames == 0:
            return

        # Create a new image with the calculated size
        atlas_width = min(cols * frame_width, max_size)
        atlas_height = min(rows * frame_height, max_size)
        atlas = Image.new("RGBA", (atlas_width, atlas_height), (0, 0, 0, 0))

        # Paste frames into the atlas (single row)
        for idx, frame_file in enumerate(frame_files):
            if idx >= cols:
                break
            frame_img = Image.open(frame_file).convert("RGBA")
            col = idx
            row = 0
            atlas.paste(frame_img, (col * frame_width, row * frame_height))
            frame_img.close()  # Close frame image to free resources

        # Save the atlas
        atlas.save(output_path)
        for frame_file in frame_files:
            if os.path.exists(frame_file):
                os.remove(frame_file)  # Clean up temporary frames

        atlas.close()  # Close atlas image to free resources

    def extract_atlas_and_audio(self):
        video_path = self.video_path.get()
        framerate = float(self.framerate.get())  # Convert to float for calculation
        resolution = self.resolution.get()

        if not video_path or not os.path.exists(video_path):
            messagebox.showerror("Error", "Please select a valid video file.")
            return

        # Create output folder based on video filename
        video_name = Path(video_path).stem
        output_dir = os.path.join(os.path.dirname(video_path), f"{video_name}_frames")
        os.makedirs(output_dir, exist_ok=True)

        # Get frame dimensions
        frame_width, frame_height = (160, 90) if resolution == "original" else tuple(map(int, resolution.split("x")))
        if resolution == "original":
            try:
                cmd = [self.ffmpeg_path, "-i", video_path, "-f", "null", "-"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                for line in result.stderr.splitlines():
                    if "Stream #0:0" in line and "Video:" in line:
                        res = line.split(",")[2].strip().split(" ")[0]
                        frame_width, frame_height = map(int, res.split("x"))
                        break
            except subprocess.CalledProcessError:
                messagebox.showerror("Error", "Could not determine video resolution.")
                return

        # Calculate number of frames
        frame_count = self.get_frame_count(video_path, framerate)

        # Step 1: Export first frame separately
        first_frame_path = os.path.join(output_dir, f"{video_name}_first_frame.png")
        first_frame_command = [
            self.ffmpeg_path, "-i", video_path,
            "-vf", "select='eq(n,0)'",
            "-s", f"{frame_width}x{frame_height}",
            "-q:v", "2",
            "-frames:v", "1",
            first_frame_path
        ]
        try:
            subprocess.run(first_frame_command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to extract first frame: {e.stderr}")
            return

        # Step 2: Extract individual frames for atlases
        frame_pattern = os.path.join(output_dir, "frame_%04d.png")
        frame_command = [
            self.ffmpeg_path, "-i", video_path,
            "-vf", f"fps={framerate}",
            "-s", f"{frame_width}x{frame_height}",
            "-q:v", "2",  # High quality
            frame_pattern
        ]
        try:
            subprocess.run(frame_command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to extract frames: {e.stderr}")
            return

        # Get extracted frame files (excluding first frame)
        frame_files = sorted([f for f in os.listdir(output_dir) if f.startswith("frame_") and f.endswith(".png")])
        frame_files = [os.path.join(output_dir, f) for f in frame_files]
        extracted_frames = len(frame_files)

        # Calculate grid size for single-row atlas
        cols, rows = self.calculate_grid(extracted_frames, frame_width, frame_height)

        # Step 3: Create single-row atlases with Pillow
        atlas_idx = 0
        while frame_files:
            batch_files = frame_files[:cols]
            frame_files = frame_files[cols:]
            output_path = os.path.join(output_dir, f"{video_name}_part{atlas_idx + 1:03d}.png")
            self.create_atlas(batch_files, output_path, cols, rows, frame_width, frame_height)
            atlas_idx += 1

        # Create frame interval file with durations
        interval_ms = 1000 / framerate  # Convert framerate to milliseconds
        in_between_duration = ((cols - 1) * interval_ms) / 1000 if cols > 1 else 0  # Duration in seconds for each atlas section
        last_batch_size = len(batch_files)  # Number of frames in the last atlas
        final_segment_duration = (last_batch_size * interval_ms) / 1000  # Duration of the final segment

        # Create Bakin event file
        bakin_event_file = os.path.join(output_dir, f"{video_name}_event.txt")
        with open(bakin_event_file, "w", encoding="utf-8") as f:
            f.write("Guid\t1cf44a05-98fd-47ed-9eab-d81428c80d2c\n")
            f.write("イベント名\t" + video_name + "\n")
            f.write("シート\tEvent Sheet\n")
            f.write("\tグラフィック\t8ac1bba5-c27b-4d96-ad27-5aa9e94daa65\n")
            f.write("\tモーション\tfirstframe\n")
            f.write("\t向き\t-1\n")
            f.write("\t向き固定\tTrue\n")
            f.write("\t物理\tFalse\n")
            f.write("\t衝突判定\tTrue\n")
            f.write("\tイベントと衝突\tTrue\n")
            f.write("\t移動速度\t0\n")
            f.write("\t移動頻度\t0\n")
            f.write("\t移動タイプ\tNONE\n")
            f.write("\t押せる\tTrue\n")
            f.write("\tスクリプト\n")
            f.write("\t\t開始条件\tTALK\n")
            f.write("\t\t高さ無視\tFalse\n")
            f.write("\t\t判定拡張\tFalse\n")

            # Add MOTION and WAIT commands for each atlas
            for i in range(atlas_idx):
                part_name = f"part{i + 1:03d}"
                f.write("\t\tコマンド\tMOTION\n")
                f.write("\t\t\tGuid\t8ac1bba5-c27b-4d96-ad27-5aa9e94daa65\n")
                f.write(f"\t\t\t文字列\t{part_name}\n")
                f.write("\t\tコマンド終了\n")
                f.write("\t\tコマンド\tWAIT\n")
                if i < atlas_idx - 1:  # Use in-between duration for all but the last part
                    f.write("\t\t\t小数\t{:.1f}\n".format(in_between_duration))
                    f.write("\t\t\t整数\t1\n")
                else:  # Use final segment duration for the last part
                    f.write("\t\t\t小数\t{:.1f}\n".format(final_segment_duration))
                    f.write("\t\t\t整数\t1\n")
                f.write("\t\tコマンド終了\n")

            # Add final MOTION to reset to firstframe
            f.write("\t\tコマンド\tMOTION\n")
            f.write("\t\t\tGuid\t8ac1bba5-c27b-4d96-ad27-5aa9e94daa65\n")
            f.write("\t\t\t文字列\tfirst_frame\n")
            f.write("\t\tコマンド終了\n")
            f.write("\tスクリプト終了\n")
            f.write("シート終了\n")

        # Create frame interval file with durations
        interval_file = os.path.join(output_dir, "frame_interval.txt")
        with open(interval_file, "w") as f:
            f.write(f"Frame interval: {interval_ms:.2f} ms (based on {framerate} fps)\n")
            f.write(f"In-between duration: {in_between_duration:.2f} seconds (per atlas section)\n")
            f.write(f"Final segment duration: {final_segment_duration:.2f} seconds (last atlas)\n")

        # Build FFmpeg command for audio extraction
        audio_output = os.path.join(output_dir, f"{video_name}_audio.wav")
        audio_command = [self.ffmpeg_path, "-i", video_path, "-vn", "-acodec", "pcm_s16le", audio_output]

        try:
            # Extract audio
            subprocess.run(audio_command, check=True, capture_output=True, text=True)

            if extracted_frames < frame_count - 1:  # Adjust for first frame being separate
                messagebox.showwarning("Warning", f"Only {extracted_frames} frames extracted out of {frame_count - 1} expected for atlases.")
            else:
                messagebox.showinfo("Success", f"Atlas images, first frame, and audio extracted to {output_dir}")
                self.root.quit()  # Force exit Tkinter loop after success
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to extract audio: {e.stderr}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FrameExtractorApp(root)
    root.mainloop()
