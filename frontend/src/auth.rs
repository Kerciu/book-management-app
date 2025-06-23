use std::ops::Deref;

#[derive(Debug, Clone, Default)]
#[repr(transparent)]
pub struct Token(String);

impl Token {
    pub fn new(data: String) -> Self {
        Self(data)
    }
}

impl Deref for Token {
    type Target = str;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

pub mod google {
    use web_sys::js_sys::{self, Object, Reflect};

    pub type Token = super::Token;

    pub fn init() {
        let params =
            web_sys::UrlSearchParams::new_with_record_from_str_to_str(&get_settings()).unwrap();
        web_sys::window()
            .unwrap()
            .location()
            .set_href(&format!(
                "{}?{}",
                env!("GOOGLE_OAUTH_URL"),
                params.to_string()
            ))
            .unwrap();
    }

    fn get_settings() -> Object {
        let crypto = web_sys::window().unwrap().crypto().unwrap();
        let state = crypto.random_uuid();
        web_sys::window()
            .unwrap()
            .local_storage()
            .unwrap()
            .unwrap()
            .set_item("google_oauth_state", &state)
            .unwrap();

        let ret = js_sys::Object::new();
        Reflect::set(&ret, &"client_id".into(), &env!("GOOGLE_CLIENT_ID").into()).unwrap();
        Reflect::set(&ret, &"scope".into(), &env!("GOOGLE_SCOPES").into()).unwrap();
        Reflect::set(
            &ret,
            &"redirect_uri".into(),
            &env!("GOOGLE_REDIRECT_URI_SIMPLE").into(),
        )
        .unwrap();
        Reflect::set(&ret, &"response_type".into(), &"code".into()).unwrap();
        Reflect::set(&ret, &"access_type".into(), &"offline".into()).unwrap();
        Reflect::set(&ret, &"state".into(), &state.into()).unwrap();
        ret
    }
}

pub mod email {
    pub type Token = super::Token;
}

pub mod github {
    use web_sys::js_sys::{Object, Reflect};

    pub type Token = super::Token;

    pub fn init() {
        let params =
            web_sys::UrlSearchParams::new_with_record_from_str_to_str(&get_settings()).unwrap();
        web_sys::window()
            .unwrap()
            .location()
            .set_href(&format!(
                "{}?{}",
                env!("GITHUB_OAUTH_URL"),
                params.to_string()
            ))
            .unwrap();
    }

    fn get_settings() -> Object {
        let crypto = web_sys::window().unwrap().crypto().unwrap();
        let state = crypto.random_uuid();
        web_sys::window()
            .unwrap()
            .local_storage()
            .unwrap()
            .unwrap()
            .set_item("github_oauth_state", &state)
            .unwrap();

        let ret = Object::new();
        Reflect::set(&ret, &"client_id".into(), &env!("GITHUB_CLIENT_ID").into()).unwrap();
        Reflect::set(
            &ret,
            &"redirect_uri".into(),
            &env!("GITHUB_REDIRECT_URI_SIMPLE").into(),
        )
        .unwrap();
        Reflect::set(&ret, &"state".into(), &state.into()).unwrap();
        ret
    }
}
