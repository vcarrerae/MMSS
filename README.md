# MMSS: Micromagnetic MacroSpin Simulator

**MMSS (Micromagnetic MacroSpin Simulator)** is an open-source finite element method (FEM) solver written in FreeFEM++[span_0](start_span)[span_0](end_span)[span_1](start_span)[span_1](end_span). It is designed to compute the magnetostatic interactions and hysteresis loops of two-dimensional Stoner-Wohlfarth particle (macrospin) arrays with arbitrary geometries[span_2](start_span)[span_2](end_span). 

By utilizing unstructured Delaunay triangulation, MMSS eliminates the artificial magnetic pinning and local field divergences (staircasing effects) typically produced by finite difference solvers over rectangular grids[span_3](start_span)[span_3](end_span)[span_4](start_span)[span_4](end_span). The software finds the magnetic equilibrium states by evaluating the weak formulation of the magnetostatic scalar potential and applying a steepest descent energy minimization algorithm[span_5](start_span)[span_5](end_span)[span_6](start_span)[span_6](end_span).

---

## 1. Theoretical Background & Formulation

### Complete Deduction of the Weak Form (Eq. 2)
To find the demagnetizing field $h_d = -\nabla u$, MMSS solves the magnetostatic scalar potential $u$ governed by $\Delta u = \nabla \cdot m$[span_7](start_span)[span_7](end_span). Multiplying by a test function $v$ and integrating over the magnetic domain $\Omega$[span_8](start_span)[span_8](end_span):
$-\int_{\Omega} v [\nabla \cdot \nabla u] dV = -\int_{\Omega} v (\nabla \cdot m) dV$

Applying Green's first identity[span_9](start_span)[span_9](end_span):
$\int_{\Omega} \nabla u \cdot \nabla v dV - \oint_{\partial \Omega} v \frac{\partial u}{\partial n} d\Gamma = \int_{\Omega} \nabla v \cdot m dV - \oint_{\partial \Omega} v (m \cdot n) d\Gamma$

Assuming single-domain particles with uniform magnetization, the volume magnetic charges vanish ($\nabla \cdot m = 0$)[span_10](start_span)[span_10](end_span). Reorganizing the terms and integrating over the entire computational cell $D$ (where $D = \Omega \cup S$) leads to the final weak formulation[span_11](start_span)[span_11](end_span)[span_12](start_span)[span_12](end_span):
$\int_{D} \nabla u \cdot \nabla v dV - \sum_{i=1}^{N} \oint_{\partial \Omega_i} v (m_i \cdot n_i) d\Gamma_i = 0$[span_13](start_span)[span_13](end_span)

### FEM Spaces and Potential Constant
* **FEM Spaces:** The numerical solution is approximated using **P1 elements** (piecewise linear continuous polynomials) over the Delaunay triangulation[span_14](start_span)[span_14](end_span).
* **Potential Constant Treatment:** The constant of the magnetostatic potential is fixed by applying a homogeneous Dirichlet boundary condition ($u = 0$) on the outer boundary of the computational cell ($\partial D$)[span_15](start_span)[span_15](end_span). 

---

## 2. Energy Minimization & Gradient Descent
Instead of solving the temporal Landau-Lifshitz-Gilbert (LLG) equations, MMSS finds the equilibrium by minimizing the dimensionless energy $\hat{E}$[span_16](start_span)[span_16](end_span):

* **Gradient Descent Algorithm:** The magnetization is updated iteratively in the direction of maximum descent using the tangential component of the energy gradient $\nabla_{m_i} \hat{E}$[span_17](start_span)[span_17](end_span)[span_18](start_span)[span_18](end_span).
* **Step Size ($\alpha$):** An adaptive line search is employed. The update is computed as $m_{k+1} = m_k + \alpha \nabla_m \hat{E}$. If the proposed step increases the total energy ($E_{k+1} > E_k$), the step size is halved ($\alpha \leftarrow \alpha/2$) and the step is rejected until energy decreases[span_19](start_span)[span_19](end_span).
* **Tolerance & Max Iterations:** The inner loop converges when the maximum $L^\infty$-norm of the tangential gradient falls below a user-defined tolerance (e.g., $10^{-5}$)[span_20](start_span)[span_20](end_span) or when it reaches the maximum number of iterations (`[Insert Max Iterations, e.g., 5000]`).
* **Field Steps & Initialization:** For each quasi-static step of the external field ($h_{ex} + \Delta h_{ex}$), the minimization algorithm is initialized using the equilibrium magnetization $m_{eq}$ from the previous field step[span_21](start_span)[span_21](end_span).
* **Hysteresis Branches:** The major hysteresis loop is constructed by performing two consecutive sweeps: a descending branch from $+h_{max}$ to $-h_{max}$, followed by an ascending branch from $-h_{max}$ to $+h_{max}$[span_22](start_span)[span_22](end_span).

---

## 3. Mesh Convergence & Cell Size Sensitivity
* **Mesh Convergence:** FreeFEM++ adaptive meshing ensures that the micromagnetic energy stabilizes as the number of nodes increases[span_23](start_span)[span_23](end_span). The user can control the mesh density parameter on the analytical boundaries.
* **Sensitivity to the Size of $D$:** Since $u=0$ is imposed on $\partial D$, the computational cell $D$ is chosen strictly large enough ($D \gg \Omega$) to prevent the artificial truncation of the demagnetizing field $h_d$ from influencing the magnetization of the particles[span_24](start_span)[span_24](end_span).

---

## 4. Minimum Reproducible Example (MRE)
To reproduce the validation case of a vertical elliptical Stoner-Wohlfarth particle (Aspect Ratio 2:1):

**1. Execution Command:**
```bash
FreeFem++ examples/ellipse_validation.edp
