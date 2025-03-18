mod colorize;

use pyo3::prelude::*;

use colorize::_Colorize;

#[pymodule]
pub fn _colorize(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<_Colorize>()?;
    Ok(())
}
