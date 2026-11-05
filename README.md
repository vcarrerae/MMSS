# MMSS: Micromagnetic MacroSpin Simulator

**MMSS (Micromagnetic MacroSpin Simulator)** is an open-source finite element method (FEM) solver written in FreeFEM++. It is designed to compute the magnetostatic interactions and hysteresis loops of two-dimensional Stoner-Wohlfarth particle (macrospin) arrays with arbitrary geometries. 

By utilizing unstructured Delaunay triangulation, MMSS eliminates the artificial magnetic pinning and local field divergences (staircasing effects) typically produced by finite difference solvers over rectangular grids. The software finds the magnetic equilibrium states by evaluating the weak formulation of the magnetostatic scalar potential and applying a steepest descent energy minimization algorithm.

---

## 1. Theoretical Background & Formulation

### Complete Deduction of the Weak Form (Eq. 2)
To find the demagnetizing field $h_d = -\nabla u$, MMSS solves the magnetostatic scalar potential $u$ governed by $\Delta u = \nabla \cdot m$. Multiplying by a test function $v$ and integrating over the magnetic domain $\Omega$:

$$-\int_{\Omega} v [\nabla \cdot \nabla u] dV = -\int_{\Omega} v (\nabla \cdot m) dV$$

Applying Green's first identity:
$$\int_{\Omega} \nabla u \cdot \nabla v dV - \oint_{\partial \Omega} v \frac{\partial u}{\partial n} d\Gamma = \int_{\Omega} \nabla v \cdot m dV - \oint_{\partial \Omega} v (m \cdot n) d\Gamma$$

Assuming single-domain particles with uniform magnetization, the volume magnetic charges vanish ($\nabla \cdot m = 0$). Reorganizing the terms and integrating over the entire computational cell $D$ (where $D = \Omega \cup S$) leads to the final weak formulation:
$$\int_{D} \nabla u \cdot \nabla v dV - \sum_{i=1}^{N} \oint_{\partial \Omega_i} v (m_i \cdot n_i) d\Gamma_i = 0$$

### FEM Spaces and Potential Constant
* **FEM Spaces:** The numerical solution is approximated using **P1 elements** (piecewise linear continuous polynomials) over the Delaunay triangulation.
* **Potential Constant Treatment:** The constant of the magnetostatic potential is fixed by applying a homogeneous Dirichlet boundary condition ($u = 0$) on the outer boundary of the computational cell ($\partial D$). 

---

## 2. Energy Minimization & Gradient Descent
Instead of solving the temporal Landau-Lifshitz-Gilbert (LLG) equations, MMSS finds the equilibrium by minimizing the dimensionless energy $\hat{E}$:

* **Gradient Descent Algorithm:** The magnetization is updated iteratively in the direction of maximum descent using the tangential component of the energy gradient $\nabla_{m_i} \hat{E}$.
* **Step Size ($\alpha$):** An adaptive line search is employed. The update is computed as $m_{k+1} = m_k + \alpha \nabla_m \hat{E}$. If the proposed step increases the total energy ($E_{k+1} > E_k$), the step size is halved ($\alpha \leftarrow \alpha/2$) and the step is rejected until energy decreases.
* **Tolerance & Max Iterations:** The inner loop converges when the maximum $L^\infty$-norm of the tangential gradient falls below a user-defined tolerance (e.g., $10^{-5}$) or when it reaches the maximum number of iterations (`[Insert Max Iterations, e.g., 5000]`).
* **Field Steps & Initialization:** For each quasi-static step of the external field ($h_{ex} + \Delta h_{ex}$), the minimization algorithm is initialized using the equilibrium magnetization $m_{eq}$ from the previous field step.
* **Hysteresis Branches:** The major hysteresis loop is constructed by performing two consecutive sweeps: a descending branch from $+h_{max}$ to $-h_{max}$, followed by an ascending branch from $-h_{max}$ to $+h_{max}$.

---

## 3. Mesh Convergence & Cell Size Sensitivity
* **Mesh Convergence:** FreeFEM++ adaptive meshing ensures that the micromagnetic energy stabilizes as the number of nodes increases. The user can control the mesh density parameter on the analytical boundaries.
* **Sensitivity to the Size of $D$:** Since $u=0$ is imposed on $\partial D$, the computational cell $D$ is chosen strictly large enough ($D \gg \Omega$) to prevent the artificial truncation of the demagnetizing field $h_d$ from influencing the magnetization of the particles.

---

## 4. Minimum Reproducible Example (MRE)
To reproduce the validation case of a vertical elliptical Stoner-Wohlfarth particle (Aspect Ratio 2:1):

**1. Execution Command:**
```bash
FreeFem++ examples/SW1P.edp
```

**2. Expected Reference Values:**
For a vertically aligned ellipse ($\phi = 0^\circ$), the expected normalized coercive field is $h_c \approx 0.33$. 

**3. Output Files:**
* `hysteresis_data.txt`: Contains columns for $h_{ex}$, total energy $\hat{E}$, and magnetization components ($M_x/M_s, M_y/M_s$).
* `potential_map.txt` / `.vtk`: Colormap data of the magnetostatic scalar potential $u(x,y)$.

**4. Regenerating Figures:**
Running SW1P.edp returns a "SW1P.txt" and "SW1P.eps". The .eps represents the geometry and magnetostatic scalar potential. Besides, the .txt file has five columns: 

$$[h_x, h_y, E, mx0, my0]$$

this is, the external field in the horizontal axis, the external field in the verical axis, the energy for the current equilibrium state for the actual value of the external field, the horizontal component of the magnetization of the first particle, and the vertical component of the magnetization of the first particle, respectively. 

To reproduce the hysteresis loop, you can plot the second column $(h_y)$ vs the fifth column $(my0)$.

---

## 5. Performance Benchmark
The steepest descent energetic approach yields a near-linear runtime scaling $t \approx 3.2 \times 10^3 N^{0.9}$. The following benchmark was executed for $N=16$ particles:

* **CPU:** `Macbook Pro M5`
* **RAM:** `16 GB DDR4]`
* **OS:** `MacOS 26`
* **FreeFEM++ Version:** `4.12`
* **Mesh points per object** `mp=200`
* **Field Step Size:** `dh = 0.002`
* **Average Runtime:** `4757sec`

---

## 6. Prerequisites & Tested Environments
**Core Solver:**
* FreeFEM++ (> v4.0).
* Cross-platform verified on: macOS, and Windows 10/11.

**Post-Processing & Visualization:**
* Python 3.8+ (Tested up to Python 3.11).
* Required Libraries: `matplotlib` (v3.5+), `pandas` (v1.4+), `numpy` (v1.22+), `seaborn` (v0.11+).

---

## 7. Authors, Citation & License
If you use MMSS in your research, please cite the associated publication:



This project is licensed under the **GNU General Public License v3.0**.
