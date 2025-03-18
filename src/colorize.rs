use pyo3::prelude::*;

#[pyclass(str)]
pub struct _Colorize {
    original: String,
    codes: Vec<u8>,
}

impl std::fmt::Display for _Colorize {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let terminal_supports_color: bool;
        {
            use supports_color::{on, Stream};
            terminal_supports_color = on(Stream::Stdout).is_some();
        }

        if self.codes.is_empty() || !terminal_supports_color {
            return write!(f, "{}", self.original);
        }

        let mut colored = String::with_capacity(
            // Reserve space for the ANSI escape sequence (1 character),
            // plus a character for each code and the semicolon separators.
            (1 + (self.codes.len() * 2 - 1))
            // In the worst case, RGB colors are used for both the foreground
            // and background, which require 3 digits each. We've already
            // reserved 1 character above for each value, so we need to add
            // 2 for each color, for both foreground and background.
            + ((2 * 3) * 2)
            // Include the length of the original string.
            + self.original.len()
            // Reserve space for the ANSI escape sequence (1 character).
            + 1
            // All reset codes, excluding 0 (which we do not use), are two
            // digits. There can be up to 3 reset codes: style, foreground,
            // and background.
            + (2 * 3),
        );

        colored.push_str("\x1B["); // ANSI escape sequence.

        let mut reset_codes = Vec::<u8>::with_capacity(6);
        let mut codes = self.codes.iter().peekable();

        while let Some(&code) = codes.by_ref().next() {
            let reset_code = match code {
                // bold and dim share a reset code.
                1 | 2 => 22,
                // The remaining styles.
                3..=5 | 7..=9 => code + 20,
                // Foreground colors.
                30..=38 => 39,
                // Background colors.
                40..=48 => 49,
                // Anything else would be a logic error.
                _ => unreachable!("invalid code: {code}"),
            };
            reset_codes.push(reset_code);
            colored.push_str(&code.to_string());

            // Handle 8-bit and 24-bit colors.
            if code == 38 || code == 48 {
                let next_code = *codes
                    .next()
                    .expect("expected 8-bit or 24-bit color sequence");
                colored.push(';');
                colored.push_str(&next_code.to_string());

                if next_code == 5 {
                    // One of the 256 8-bit color values.
                    colored.push(';');
                    colored.push_str(&*codes.next().unwrap().to_string());
                } else if next_code == 2 {
                    // Red
                    colored.push(';');
                    colored.push_str(&*codes.next().unwrap().to_string());
                    // Green
                    colored.push(';');
                    colored.push_str(&*codes.next().unwrap().to_string());
                    // Blue
                    colored.push(';');
                    colored.push_str(&*codes.next().unwrap().to_string());
                } else {
                    unreachable!()
                }
            }

            if let Some(_) = codes.peek() {
                colored.push(';');
            }
        }
        colored.push('m');
        colored.push_str(&self.original);

        colored.push_str("\x1B["); // ANSI escape sequence.
        // We already know there is at least one reset code.
        let last = reset_codes.pop().unwrap();
        for reset_code in reset_codes.iter() {
            colored.push_str(&reset_code.to_string());
            colored.push(';');
        }
        colored.push_str(&last.to_string());
        colored.push('m');

        write!(f, "{}", colored)
    }
}

#[pymethods]
impl _Colorize {
    #[new]
    fn new(s: String) -> Self {
        Self {
            original: s,
            codes: Vec::new(),
        }
    }

    fn bold(&mut self) {
        self.codes.push(1);
    }

    fn dim(&mut self) {
        self.codes.push(2);
    }

    fn italic(&mut self) {
        self.codes.push(3);
    }

    fn underline(&mut self) {
        self.codes.push(4);
    }

    fn blink(&mut self) {
        self.codes.push(5);
    }

    fn inverse(&mut self) {
        self.codes.push(7);
    }

    fn hidden(&mut self) {
        self.codes.push(8);
    }

    fn strikethrough(&mut self) {
        self.codes.push(9);
    }

    fn black(&mut self) {
        self.codes.push(30);
    }

    fn red(&mut self) {
        self.codes.push(31);
    }

    fn green(&mut self) {
        self.codes.push(32);
    }

    fn yellow(&mut self) {
        self.codes.push(33);
    }

    fn blue(&mut self) {
        self.codes.push(34);
    }

    fn magenta(&mut self) {
        self.codes.push(35);
    }

    fn cyan(&mut self) {
        self.codes.push(36);
    }

    fn white(&mut self) {
        self.codes.push(37);
    }

    fn color256(&mut self, color: u8) {
        self.codes.push(38);
        self.codes.push(5);
        self.codes.push(color);
    }

    fn true_color(&mut self, red: u8, green: u8, blue: u8) {
        self.codes.push(38);
        self.codes.push(2);
        self.codes.push(red);
        self.codes.push(green);
        self.codes.push(blue);
    }

    fn on_black(&mut self) {
        self.codes.push(40);
    }

    fn on_red(&mut self) {
        self.codes.push(41);
    }

    fn on_green(&mut self) {
        self.codes.push(42);
    }

    fn on_yellow(&mut self) {
        self.codes.push(43);
    }

    fn on_blue(&mut self) {
        self.codes.push(44);
    }

    fn on_magenta(&mut self) {
        self.codes.push(45);
    }

    fn on_cyan(&mut self) {
        self.codes.push(46);
    }

    fn on_white(&mut self) {
        self.codes.push(47);
    }

    fn on_color256(&mut self, color: u8) {
        self.codes.push(48);
        self.codes.push(5);
        self.codes.push(color);
    }

    fn on_true_color(&mut self, red: u8, green: u8, blue: u8) {
        self.codes.push(48);
        self.codes.push(2);
        self.codes.push(red);
        self.codes.push(green);
        self.codes.push(blue);
    }
}
