import os
import sys
import shutil
import subprocess
from pathlib import Path
from random import randint


def reload_editor_plugin():
    # define useful paths
    script_directory = Path(os.path.dirname(os.path.abspath(sys.argv[0])))
    target_dir = script_directory.joinpath("target")
    release_dir = target_dir.joinpath("release")
    synthic_path = target_dir.joinpath("polygen", "SynthicNative.cs")
    unity_synthic_dir = script_directory.joinpath("..", "..", "Assets", "Synthic")
    unity_native_dir = unity_synthic_dir.joinpath("Native")
    unity_plugin_dir = unity_native_dir.joinpath("Plugins")
    unity_synthic_path = unity_native_dir.joinpath("SynthicNative.cs")

    # clean and rebuild the cargo project
    print(f"Rebuilding `synthic` library...")
    subprocess.run("cargo clean -p synthic --release", shell=True, cwd=script_directory)
    subprocess.run("cargo build --release", shell=True, cwd=script_directory)
    subprocess.run("cargo test --release", shell=True, cwd=script_directory)

    # try to copy every type of editor plugin
    # set a random id to each plugin so that overloads the previous
    print("Copying `synthic` library files...")
    if unity_plugin_dir.exists():
        shutil.rmtree(unity_plugin_dir)
    unity_plugin_dir.mkdir(parents=True, exist_ok=True)
    random_id = str(randint(0, 9999)).rjust(4, "0")
    lib_dll = release_dir.joinpath("synthic.dll")
    unity_dll = unity_plugin_dir.joinpath(f"synthic-{random_id}.dll")
    lib_so = release_dir.joinpath("libsynthic.so")
    unity_so = unity_plugin_dir.joinpath(f"libsynthic-{random_id}.so")
    lib_dylib = release_dir.joinpath("libsynthic.dylib")
    unity_dylib = unity_plugin_dir.joinpath(f"libsynthic-{random_id}.dylib")
    if lib_dll.is_file():
        shutil.copy(lib_dll, unity_dll)
    if lib_so.is_file():
        shutil.copy(lib_so, unity_so)
    if lib_dylib.is_file():
        shutil.copy(lib_dylib, unity_dylib)

    # replace the synthic lib name to match randomly generated id
    print("Copying `synthic` binding files...")
    with open(synthic_path) as reader:
        cs_text = reader.read()
        cs_text = cs_text.replace(
            '[DllImport("synthic"',
            f'[DllImport("synthic-{random_id}"',
        )
    with open(unity_synthic_path, "w+") as writer:
        writer.write(cs_text)


if __name__ == "__main__":
    reload_editor_plugin()
