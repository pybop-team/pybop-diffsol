use numpy::{PyArray2, PyReadonlyArray1};
use pyo3::prelude::*;

use crate::{Config, Diffsol, PyDiffsolError};

type M = diffsol::FaerSparseMat<f64>;
type LS = diffsol::FaerSparseLU<f64>;

#[pyclass]
pub(crate) struct DiffsolSparse(Diffsol<M>);

#[pymethods]
impl DiffsolSparse {
    #[new]
    fn new(code: &str, config: &Config) -> Result<Self, PyDiffsolError> {
        let inner = Diffsol::new(code, config)?;
        Ok(Self(inner))
    }

    #[pyo3(signature = (params))]
    fn set_params<'py>(&mut self, params: PyReadonlyArray1<'py, f64>) -> Result<(), PyDiffsolError> {
        self.0.set_params(params)
    }

    #[pyo3(signature = (times))]
    fn solve<'py>(&mut self, py: Python<'py>, times: PyReadonlyArray1<'py, f64>) -> Result<Bound<'py, PyArray2<f64>>, PyDiffsolError> {
        Diffsol::solve::<LS>(&mut self.0, py, times)
    }
}