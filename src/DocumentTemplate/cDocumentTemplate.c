/*****************************************************************************

  Copyright (c) 2002 Zope Foundation and Contributors.
  
  This software is subject to the provisions of the Zope Public License,
  Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
  WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
  WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
  FOR A PARTICULAR PURPOSE
  
 ****************************************************************************/
static char cDocumentTemplate_module_documentation[] = 
""
;

#include "ExtensionClass/ExtensionClass.h"

/* ----------------------------------------------------- */

static struct PyMethodDef Module_Level__methods[] = {
  {NULL, (PyCFunction)NULL, 0, NULL}		/* sentinel */
};

void
initcDocumentTemplate(void)
{
  PyObject *m, *d;

  m = Py_InitModule4("cDocumentTemplate", Module_Level__methods,
		     cDocumentTemplate_module_documentation,
		     (PyObject*)NULL,PYTHON_API_VERSION);

  d = PyModule_GetDict(m);
}
