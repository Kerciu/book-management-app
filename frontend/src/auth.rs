pub mod google {
    use std::any::TypeId;
    use wasm_bindgen::prelude::*;
    use web_sys::js_sys::{self, Reflect};

    #[wasm_bindgen]
    unsafe extern "C" {
        pub type Handle;

        #[wasm_bindgen(js_namespace = gapi, js_name = load)]
        fn load_auth(auth: &str, then: &Closure<dyn Fn()>);

        #[wasm_bindgen(js_namespace = ["gapi", "auth2"], js_name = init)]
        fn init_auth(settings: JsValue) -> JsValue;
    }

    fn prop_key() -> JsValue {
        format!("{:?}__GOOGLE_AUTH", TypeId::of::<Handle>()).into()
    }

    /// initializes Google OAuth object and stores it in global context
    #[wasm_bindgen(js_name = init_google_auth)]
    pub fn init() {
        // TODO: should we use synchronization here?
        //       or just optimistically assume Auth will be ready
        //       by the time we need it?
        let callback = Closure::new(move || {
            let args = js_sys::Object::new();
            // TODO: Error handling
            let _ = js_sys::Reflect::set(&args, &"client_id".into(), &"TODO".into());
            // TODO: Scope

            let auth: Handle = init_auth(args.into()).into();
            let _ = Reflect::set(&web_sys::window().unwrap(), &prop_key(), &auth);
        });
        load_auth("auth2", &callback);
    }

    pub fn get_handle() -> Handle {
        js_sys::Reflect::get(&web_sys::window().unwrap(), &prop_key())
            .unwrap()
            .into()
    }
}

pub mod email {
    #[derive(Debug, Clone)]
    pub struct Token(String);

    impl Token {
        pub fn new(token: String) -> Self {
            Self(token)
        }
    }
}
