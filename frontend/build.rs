//! This file will supply .env file to rustc, so we don't have to provide it
//! to client, and the final binary will only have used variables, avoiding
//! secrets leakage.

use dotenv::{dotenv, vars};

fn main() {
    let path = dotenv().unwrap();
    println!("cargo::rerun-if-changed={}", path.display());

    for (key, value) in vars() {
        println!("cargo::rustc-env={key}={value}")
    }
}
