#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>

#include "calculate-loss.h"

extern "C" {PyObject *calculate_loss_wrapper(void *, PyObject *, PyObject *);}
PyObject * calculate_loss_wrapper(PyObject * self, PyObject * args)
{
  int n_years;
  double florida_rate;
  double florida_mean;
  double florida_stddev;

  double gulf_rate;
  double gulf_mean;
  double gulf_stddev;

  double result;

  // parse arguments
  if (!PyArg_ParseTuple(args, "idddddd", &n_years,
                    &florida_rate, &florida_mean, &florida_stddev,
                    &gulf_rate, &gulf_mean, &gulf_stddev)) {
    return NULL;
  }

  result = calculate_loss(n_years, florida_rate, florida_mean, florida_stddev,
                                  gulf_rate, gulf_mean, gulf_stddev);

  return PyLong_FromDouble(result);
}

/**
 * List of methods to export.
 */
static PyMethodDef LossFrameworkMethods[] = {
 { "calculate_loss", calculate_loss_wrapper, METH_VARARGS, "Calculates total loss due to hurricanes in Florida and the Gulf States." },
 { NULL, NULL, 0, NULL }
};

/**
 * Definition of this Module.
 */
static struct PyModuleDef _lossFrameworkModule =
{
    PyModuleDef_HEAD_INIT,
    "loss_framework",
    "Example Framework for calculating loss.",
    -1,
    (PyMethodDef *)LossFrameworkMethods
};

/**
 * The initialization function that python will look for.
 */
PyMODINIT_FUNC PyInit_loss_framework(void)
{
    return PyModule_Create(&_lossFrameworkModule);
}
