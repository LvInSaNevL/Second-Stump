from scenedetect import VideoManager
from scenedetect import SceneManager
from scenedetect import video_splitter
from scenedetect.detectors import ContentDetector

# Mostly boiler plate code provided by SceneDetect
# https://pyscenedetect.readthedocs.io/en/latest/examples/usage-python/
def find_scenes(video_path, threshold=30.0):
    # Create our video & scene managers, then add the detector.
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(
        ContentDetector(threshold=threshold))

    # Base timestamp at frame 0 (required to obtain the scene list).
    base_timecode = video_manager.get_base_timecode()

    # Improve processing speed by downscaling before processing.
    video_manager.set_downscale_factor()

    # Start the video manager and perform the scene detection.
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)

    # Each returned scene is a tuple of the (start, end) timecode.
    return scene_manager.get_scene_list(base_timecode)


def split_video(input_video_paths, scene_list, output_file_template,
                         video_name, suppress_output=False):
    if not input_video_paths or not scene_list:
        return

    ret_val = None
    # mkvmerge automatically appends '-$SCENE_NUMBER'.
    output_file_name = output_file_template.replace('-${SCENE_NUMBER}', '')
    output_file_name = output_file_template.replace('-$SCENE_NUMBER', '')
    output_file_template = Template(output_file_name)
    output_file_name = output_file_template.safe_substitute(
        VIDEO_NAME=video_name,
        SCENE_NUMBER='')

    try:
        call_list = ['mkvmerge']
        if suppress_output:
            call_list.append('--quiet')
        call_list += [
            '-o', output_file_name,
            '--split',
            'parts:%s' % ','.join(
                ['%s-%s' % (start_time.get_timecode(), end_time.get_timecode())
                 for start_time, end_time in scene_list]),
            ' +'.join(input_video_paths)]
        total_frames = scene_list[-1][1].get_frames() - scene_list[0][0].get_frames()
        processing_start_time = time.time()
        ret_val = invoke_command(call_list)
        if not suppress_output:
            print('')
    except CommandTooLong:
        logging.error(COMMAND_TOO_LONG_STRING)
    if ret_val is not None and ret_val != 0:

# Handles cutting the complilation into smaller, useable chunks
def cut_video(video_path):
    scenes = find_scenes("data/rawVideos/{}".format(video_path))
    print("{0} number of scenes detected: {1}".format(video_path, len(scenes)))
    # Finally splits the video into clips
    split_video(
        "data/rawVideos/{}".format(video_path),
        scenes,
        "data/rawClipsVz/Scenes\\Scene.mkv",
        video_path,
        suppress_output=False,
    )

