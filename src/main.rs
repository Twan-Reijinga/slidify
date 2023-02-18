extern crate rspotify;

use std::collections::HashMap;
use std::env;

use dotenv::dotenv;
use rspotify::blocking::client::Spotify;
use rspotify::blocking::oauth2::{ SpotifyClientCredentials, SpotifyOAuth };
use rspotify::senum::Country;

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

fn main() -> Result<()> {
    dotenv().ok();

    let env_vars = env::vars().collect::<HashMap<_, _>>();
    let client_id = env_vars.get("RSPOTIFY_CLIENT_ID").ok_or("missing RSPOTIFY_CLIENT_ID in env")?;
    let client_secret = env_vars
        .get("RSPOTIFY_CLIENT_SECRET")
        .ok_or("missing RSPOTIFY_CLIENT_SECRET in env")?;
    // for (key, _value) in env_vars.iter() {
    //     println!("{:?}", key);
    // }

    let client_credentials = SpotifyClientCredentials::default()
        .client_id(client_id)
        .client_secret(client_secret)
        .build();

    println!("{}", client_credentials.get_access_token());

    let spotify = Spotify::default().client_credentials_manager(client_credentials).build();

    // match spotify.me() {
    //     Ok(user_profile) => println!("{:?}", user_profile),
    //     Err(error) => println!("{:?}", error),
    // }

    let birdy_uri = "spotify:artist:2WX2uTcsvV5OnS0inACecP";
    let tracks = spotify.artist_top_tracks(birdy_uri, Country::UnitedStates);
    println!("{:#?}", tracks);

    Ok(())
}