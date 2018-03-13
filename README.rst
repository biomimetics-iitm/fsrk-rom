This repository consists of a Python implementation of a frequency domain
Reduced Order Model (ROM) for second-order systems with frequency dependent
system matrices, called Frequency dependent second-order Rational Krylov
(FSRK) [jith2018]_.

It can be applied to systems of the form

.. math::

   -\omega^2 \mathbf M(\omega) \mathbf x + i \omega \mathbf C(\omega) \mathbf x
   + \mathbf K(\omega) \mathbf x = \mathbf f,

where :math:`\mathbf M, \mathbf C, \mathbf K` are *frequency dependent* mass,
damping and stiffness matrices.

FSRK ROM is implemented as a class in the file ``fsrk.py``. The current
implementation was made for systems with non-viscous damping. Therefore, it
only considers the damping matrix to be frequency dependent. It can be easily
extended if needed (feel free to open up an issue).

The usage of the ROM has been demonstrated in ``main.py``. A toy problem
consisting of serially connected spring-mass-damper units (of order 500) is
reduced using the FSRK ROM. The performance of the ROM is compared with the
existing modal projection based multi-model ROM (``multimodel.py``)
[balmes1997]_.


References
----------

.. [jith2018] Jith J. and Sarkar S. A Frequency Domain Model Order Reduction
   Technique for Second-Order Systems with Nonlinear Frequency Dependent
   Damping. Submitted to Computer methods in Applied Mechanics and Engineering,
   2018.

.. [balmes1997] Balmès E. Model Reduction for Systems with Frequency Dependent
   Damping Properties. Proceedings of the 15th International Modal Analysis
   Conference, vol. 3089, 1997, p. 223.
