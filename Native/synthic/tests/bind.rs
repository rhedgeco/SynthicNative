use std::{fs, path::PathBuf};

use polygen::PolyBag;
use polygen_csharp::CSharpRenderer;
use synthic::SynthicEngine;

static OUTPUT_DIR: &str = "target/polygen";

#[test]
fn bind() {
    // clear output folder
    let out_path = PathBuf::from(OUTPUT_DIR);
    if out_path.exists() {
        fs::remove_dir_all(out_path).unwrap();
    }

    // create the PolyBag
    let bag = PolyBag::new("Native").register_impl::<SynthicEngine>();

    // render the csharp data to a file
    fs::create_dir_all(OUTPUT_DIR).unwrap();
    fs::write(
        PathBuf::from(OUTPUT_DIR).join("SynthicNative.cs"),
        CSharpRenderer {
            lib_name: "synthic".to_string(),
            namespace: "Synthic".to_string(),
        }
        .render(&bag),
    )
    .unwrap();
}
