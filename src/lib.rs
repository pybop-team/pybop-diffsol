pub(crate) mod error;
pub(crate) mod config;
pub(crate) mod problem;
pub(crate) mod dense;
pub(crate) mod sparse;

pub(crate) use config::Config;
pub(crate) use error::PyDiffsolError;
pub(crate) use problem::Diffsol;
pub(crate) use dense::DiffsolDense;
pub(crate) use sparse::DiffsolSparse;

use pyo3::prelude::*;

#[pymodule]
fn pybop_diffsol(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<DiffsolDense>()?;
    m.add_class::<DiffsolSparse>()?;
    m.add_class::<Config>()?;
    Ok(())
}
