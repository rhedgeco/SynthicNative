use polygen::polygen;

#[polygen]
pub struct SynthicEngine {
    item: u32,
}

#[polygen]
impl SynthicEngine {
    pub fn new() -> Self {
        Self { item: 42 }
    }
}
