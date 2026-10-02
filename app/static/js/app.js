/**
 * AI-Powered Resume Scorer - Interactive Client Application
 * Features: Multi-format OCR (JPG/PNG/PDF), Universal Company Intelligence,
 * Candidate Experience Level Modeling (Fresher vs Experienced), and Roadmap Generation.
 */

document.addEventListener("DOMContentLoaded", () => {
  // Application State
  let currentFile = null;
  let extractedFileText = "";
  let sampleRolesData = [];
  let latestScoreResult = null;
  let currentExperienceType = "fresher";
  let currentCompanyIntel = null;

  // Header Elements
  const engineStatusText = document.getElementById("engineStatusText");
  const sampleButtonsContainer = document.getElementById("sampleButtonsContainer");

  // Profile Settings Elements
  const btnFresher = document.getElementById("btnFresher");
  const btnExperienced = document.getElementById("btnExperienced");
  const expYearsContainer = document.getElementById("expYearsContainer");
  const yearsSelect = document.getElementById("yearsSelect");
  const roleSelect = document.getElementById("roleSelect");

  // Resume Upload / Paste Tabs
  const tabUpload = document.getElementById("tabUpload");
  const tabPaste = document.getElementById("tabPaste");
  const uploadView = document.getElementById("uploadView");
  const pasteView = document.getElementById("pasteView");

  const dropzone = document.getElementById("dropzone");
  const resumeFileInput = document.getElementById("resumeFileInput");
  const btnBrowseFile = document.getElementById("btnBrowseFile");
  const fileInfoCard = document.getElementById("fileInfoCard");
  const previewFileName = document.getElementById("previewFileName");
  const previewFileMeta = document.getElementById("previewFileMeta");
  const btnRemoveFile = document.getElementById("btnRemoveFile");
  const resumeTextInput = document.getElementById("resumeTextInput");
  const resumeWordCount = document.getElementById("resumeWordCount");

  // Company Intelligence & JD Elements
  const tabCompanyMode = document.getElementById("tabCompanyMode");
  const tabCustomJd = document.getElementById("tabCustomJd");
  const companyModeView = document.getElementById("companyModeView");
  const customJdView = document.getElementById("customJdView");

  const targetCompanyInput = document.getElementById("targetCompanyInput");
  const btnFetchIntel = document.getElementById("btnFetchIntel");
  const popularChipsContainer = document.getElementById("popularChipsContainer");
  const jdTextInput = document.getElementById("jdTextInput");
  const jdWordCount = document.getElementById("jdWordCount");

  // Company Preview Card
  const previewCompName = document.getElementById("previewCompName");
  const previewCompTier = document.getElementById("previewCompTier");
  const previewCompRole = document.getElementById("previewCompRole");
  const previewExamSummary = document.getElementById("previewExamSummary");
  const previewCgpa = document.getElementById("previewCgpa");
  const previewDsa = document.getElementById("previewDsa");

  // Action & Loading Elements
  const btnScoreResume = document.getElementById("btnScoreResume");
  const loadingState = document.getElementById("loadingState");
  const resultsContainer = document.getElementById("resultsContainer");

  // Results Overview Elements
  const gaugeProgress = document.getElementById("gaugeProgress");
  const resOverallScore = document.getElementById("resOverallScore");
  const resGradeBadge = document.getElementById("resGradeBadge");
  const resExpBadge = document.getElementById("resExpBadge");
  const resSummary = document.getElementById("resSummary");

  const resSemanticScore = document.getElementById("resSemanticScore");
  const resSkillScore = document.getElementById("resSkillScore");
  const resReqScore = document.getElementById("resReqScore");
  const resAtsScore = document.getElementById("resAtsScore");

  const fillSemantic = document.getElementById("fillSemantic");
  const fillSkill = document.getElementById("fillSkill");
  const fillReq = document.getElementById("fillReq");
  const fillAts = document.getElementById("fillAts");

  // Company Roadmap Elements
  const roadmapCompanyTitle = document.getElementById("roadmapCompanyTitle");
  const roadmapStatusBadge = document.getElementById("roadmapStatusBadge");
  const roadmapEligibilityList = document.getElementById("roadmapEligibilityList");
  const roadmapExpectationsList = document.getElementById("roadmapExpectationsList");
  const roadmapGapsList = document.getElementById("roadmapGapsList");
  const examRoundsList = document.getElementById("examRoundsList");
  const mustHaveList = document.getElementById("mustHaveList");

  // Skills & Tips Elements
  const matchedSkillsCount = document.getElementById("matchedSkillsCount");
  const missingSkillsCount = document.getElementById("missingSkillsCount");
  const matchedSkillsTags = document.getElementById("matchedSkillsTags");
  const missingSkillsTags = document.getElementById("missingSkillsTags");
  const categoryTableBody = document.getElementById("categoryTableBody");

  const improvementTipsList = document.getElementById("improvementTipsList");
  const suggestedBulletsList = document.getElementById("suggestedBulletsList");
  const requirementsTableBody = document.getElementById("requirementsTableBody");

  const atsSectionsList = document.getElementById("atsSectionsList");
  const atsMetricsList = document.getElementById("atsMetricsList");
  const atsVerbsList = document.getElementById("atsVerbsList");
  const atsContactList = document.getElementById("atsContactList");

  const btnExportJson = document.getElementById("btnExportJson");
  const btnPrintReport = document.getElementById("btnPrintReport");

  // 1. Initial Application Setup
  initApp();

  async function initApp() {
    // Check Health
    try {
      const res = await fetch("/api/health");
      if (res.ok) {
        const data = await res.json();
        engineStatusText.textContent = `${data.semantic_engine} & OCR Active`;
      }
    } catch (e) {
      console.warn("Health check error:", e);
    }

    // Load Sample Roles
    try {
      const res = await fetch("/api/sample-data");
      if (res.ok) {
        sampleRolesData = await res.json();
        setupSampleButtons();
      }
    } catch (e) {
      console.warn("Failed to load sample roles:", e);
    }

    // Initial Company Intelligence fetch for Google
    fetchCompanyIntelligence("Google");
  }

  // 2. Candidate Profile Toggles (Fresher vs Experienced)
  btnFresher.addEventListener("click", () => {
    currentExperienceType = "fresher";
    btnFresher.classList.add("active");
    btnExperienced.classList.remove("active");
    expYearsContainer.classList.add("hidden");
    refreshCompanyIntel();
  });

  btnExperienced.addEventListener("click", () => {
    currentExperienceType = "experienced";
    btnExperienced.classList.add("active");
    btnFresher.classList.remove("active");
    expYearsContainer.classList.remove("hidden");
    refreshCompanyIntel();
  });

  yearsSelect.addEventListener("change", () => refreshCompanyIntel());
  roleSelect.addEventListener("change", () => refreshCompanyIntel());

  function refreshCompanyIntel() {
    const comp = targetCompanyInput.value.trim() || "Google";
    fetchCompanyIntelligence(comp);
  }

  // 3. Tab Switching: Upload vs Paste
  tabUpload.addEventListener("click", () => {
    tabUpload.classList.add("active");
    tabPaste.classList.remove("active");
    uploadView.classList.remove("hidden");
    pasteView.classList.add("hidden");
  });

  tabPaste.addEventListener("click", () => {
    tabPaste.classList.add("active");
    tabUpload.classList.remove("active");
    pasteView.classList.remove("hidden");
    uploadView.classList.add("hidden");
  });

  // Tab Switching: Company Auto-Discovery vs Custom JD
  tabCompanyMode.addEventListener("click", () => {
    tabCompanyMode.classList.add("active");
    tabCustomJd.classList.remove("active");
    companyModeView.classList.remove("hidden");
    customJdView.classList.add("hidden");
  });

  tabCustomJd.addEventListener("click", () => {
    tabCustomJd.classList.add("active");
    tabCompanyMode.classList.remove("active");
    customJdView.classList.remove("hidden");
    companyModeView.classList.add("hidden");
  });

  // 4. Popular Company Chips & Search
  popularChipsContainer.querySelectorAll(".company-chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      popularChipsContainer.querySelectorAll(".company-chip").forEach((c) => c.classList.remove("active"));
      chip.classList.add("active");
      targetCompanyInput.value = chip.getAttribute("data-name");
      fetchCompanyIntelligence(chip.getAttribute("data-name"));
    });
  });

  btnFetchIntel.addEventListener("click", () => {
    const comp = targetCompanyInput.value.trim();
    if (comp) fetchCompanyIntelligence(comp);
  });

  targetCompanyInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      const comp = targetCompanyInput.value.trim();
      if (comp) fetchCompanyIntelligence(comp);
    }
  });

  async function fetchCompanyIntelligence(companyName) {
    const years = currentExperienceType === "fresher" ? 0 : parseFloat(yearsSelect.value);
    const role = roleSelect.value;

    try {
      previewCompName.textContent = `Discovering ${companyName}...`;
      const url = `/api/company-intel?company=${encodeURIComponent(companyName)}&experience_type=${currentExperienceType}&years=${years}&role=${encodeURIComponent(role)}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error("Could not retrieve company profile");

      const profile = await res.json();
      currentCompanyIntel = profile;

      // Update preview card
      previewCompName.textContent = profile.company_name;
      previewCompTier.textContent = `${profile.tier} • ${profile.industry}`;
      previewCompRole.textContent = profile.target_role;

      previewExamSummary.textContent = `${profile.exam_pattern.length} Rounds (${profile.exam_pattern.map((r) => r.name.split(" ")[0]).join(" + ")})`;
      previewCgpa.textContent = profile.eligibility_criteria.cgpa_min || "Standard Academic Standing";
      previewDsa.textContent = profile.coding_expectations.dsa_difficulty || "Standard Problem Solving";

      // If user switches to custom JD, pre-fill it with this discovered JD
      if (!jdTextInput.value.trim()) {
        jdTextInput.value = profile.target_job_description;
        updateWordCount(jdTextInput, jdWordCount);
      }
    } catch (e) {
      console.warn("Company discovery error:", e);
      previewCompName.textContent = companyName;
      previewCompTier.textContent = "Global Technology Enterprise";
    }
  }

  // 5. Sample Roles 1-Click Buttons
  function setupSampleButtons() {
    const buttons = sampleButtonsContainer.querySelectorAll(".sample-btn");
    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const roleId = btn.getAttribute("data-role");
        const companyName = btn.getAttribute("data-company") || "Google";
        const role = sampleRolesData.find((r) => r.id === roleId);
        if (!role) return;

        // Set company
        targetCompanyInput.value = companyName;
        fetchCompanyIntelligence(companyName);

        // Populate JD & Resume
        jdTextInput.value = role.job_description;
        updateWordCount(jdTextInput, jdWordCount);

        // Switch to Paste tab and populate Resume
        tabPaste.click();
        resumeTextInput.value = role.sample_resume;
        updateWordCount(resumeTextInput, resumeWordCount);

        clearUploadedFile();

        buttons.forEach((b) => (b.style.borderColor = "var(--border-strong)"));
        btn.style.borderColor = "var(--accent-primary)";
      });
    });
  }

  // 6. File Upload (PDF, Word, Text, JPG, PNG Image OCR)
  btnBrowseFile.addEventListener("click", () => resumeFileInput.click());
  dropzone.addEventListener("click", (e) => {
    if (e.target !== btnBrowseFile) resumeFileInput.click();
  });

  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  });

  dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("dragover");
  });

  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
    if (e.dataTransfer.files.length > 0) {
      handleFileSelected(e.dataTransfer.files[0]);
    }
  });

  resumeFileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 0) {
      handleFileSelected(e.target.files[0]);
    }
  });

  async function handleFileSelected(file) {
    const validExtensions = [".pdf", ".docx", ".txt", ".jpg", ".jpeg", ".png", ".webp", ".bmp"];
    const ext = "." + file.name.split(".").pop().toLowerCase();
    if (!validExtensions.includes(ext)) {
      alert("Unsupported file format. Please upload a PDF, Word (.docx), Image (.jpg, .png), or Text (.txt) file.");
      return;
    }

    currentFile = file;

    fileInfoCard.classList.remove("hidden");
    previewFileName.textContent = file.name;
    const isImage = [".jpg", ".jpeg", ".png", ".webp", ".bmp"].includes(ext);
    previewFileMeta.textContent = isImage
      ? "Running Optical Character Recognition (OCR) on image..."
      : "Extracting document text and metadata...";

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/api/extract-text", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Failed to extract text");
      }

      const data = await res.json();
      extractedFileText = data.text;
      const fileTypeLabel = isImage ? "IMAGE OCR" : data.filename.split(".").pop().toUpperCase();
      previewFileMeta.textContent = `${fileTypeLabel} • ${data.page_count} page • ${data.word_count.toLocaleString()} words extracted`;

      // Update text input in sync
      resumeTextInput.value = data.text;
      updateWordCount(resumeTextInput, resumeWordCount);
    } catch (e) {
      alert(`Text Extraction Error: ${e.message}`);
      clearUploadedFile();
    }
  }

  function clearUploadedFile() {
    currentFile = null;
    extractedFileText = "";
    resumeFileInput.value = "";
    fileInfoCard.classList.add("hidden");
  }

  btnRemoveFile.addEventListener("click", (e) => {
    e.stopPropagation();
    clearUploadedFile();
  });

  // Word Counters
  function updateWordCount(textarea, counterElem) {
    const text = textarea.value.trim();
    const count = text ? text.split(/\s+/).length : 0;
    counterElem.textContent = `${count.toLocaleString()} words`;
  }

  resumeTextInput.addEventListener("input", () => updateWordCount(resumeTextInput, resumeWordCount));
  jdTextInput.addEventListener("input", () => updateWordCount(jdTextInput, jdWordCount));

  // 7. Score Resume & Company Intelligence Request
  btnScoreResume.addEventListener("click", async () => {
    const isCompanyMode = tabCompanyMode.classList.contains("active");
    const targetComp = targetCompanyInput.value.trim();
    const customJd = jdTextInput.value.trim();

    if (isCompanyMode && !targetComp) {
      alert("Please enter a Target Company Name (e.g. Google, TCS, Amazon).");
      targetCompanyInput.focus();
      return;
    }
    if (!isCompanyMode && (!customJd || customJd.length < 20)) {
      alert("Please enter a Target Job Description (at least 20 characters).");
      jdTextInput.focus();
      return;
    }

    const hasFile = currentFile !== null;
    const pastedText = resumeTextInput.value.trim();

    if (!hasFile && (!pastedText || pastedText.length < 20)) {
      alert("Please upload a resume file (PDF/Word/JPG/PNG) or paste the resume text.");
      return;
    }

    const years = currentExperienceType === "fresher" ? 0.0 : parseFloat(yearsSelect.value);
    const targetRole = roleSelect.value;

    // Loading UI
    loadingState.classList.remove("hidden");
    resultsContainer.classList.add("hidden");
    btnScoreResume.disabled = true;
    loadingState.scrollIntoView({ behavior: "smooth", block: "center" });

    try {
      let responseData;

      if (hasFile && tabUpload.classList.contains("active")) {
        // Multipart Upload
        const formData = new FormData();
        formData.append("resume_file", currentFile);
        if (targetComp) formData.append("target_company", targetComp);
        if (customJd) formData.append("job_description", customJd);
        formData.append("experience_type", currentExperienceType);
        formData.append("years_of_experience", years.toString());
        formData.append("target_role", targetRole);

        const res = await fetch("/api/score-upload", {
          method: "POST",
          body: formData,
        });

        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.detail || "Scoring failed");
        }
        responseData = await res.json();
      } else {
        // JSON Payload
        const textToScore = pastedText || extractedFileText;
        const res = await fetch("/api/score", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            resume_text: textToScore,
            target_company: targetComp || null,
            job_description: customJd || null,
            experience_type: currentExperienceType,
            years_of_experience: years,
            target_role: targetRole,
          }),
        });

        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.detail || "Scoring failed");
        }
        responseData = await res.json();
      }

      latestScoreResult = responseData;
      renderResults(responseData);
    } catch (e) {
      alert(`Scoring Error: ${e.message}`);
    } finally {
      loadingState.classList.add("hidden");
      btnScoreResume.disabled = false;
    }
  });

  // 8. Render Results Dashboard
  function renderResults(data) {
    resultsContainer.classList.remove("hidden");
    resultsContainer.scrollIntoView({ behavior: "smooth", block: "start" });

    // 1. Overall Score & Gauge
    const score = Math.round(data.overall_score);
    animateScoreGauge(score);

    // Grade, Track & Summary
    resGradeBadge.textContent = data.grade;
    applyGradeStyle(data.grade, resGradeBadge);

    const isFresher = data.experience_type === "fresher" || data.years_of_experience < 1.5;
    resExpBadge.textContent = isFresher
      ? "🎓 Fresher Track"
      : `💼 ${Math.round(data.years_of_experience)}+ Yrs Exp Track`;

    resSummary.textContent = data.summary;

    // 2. Sub-Scores
    const sub = data.sub_scores;
    resSemanticScore.textContent = `${sub.semantic_similarity}%`;
    fillSemantic.style.width = `${sub.semantic_similarity}%`;

    resSkillScore.textContent = `${sub.skill_match}%`;
    fillSkill.style.width = `${sub.skill_match}%`;

    resReqScore.textContent = `${sub.requirement_coverage}%`;
    fillReq.style.width = `${sub.requirement_coverage}%`;

    resAtsScore.textContent = `${sub.ats_health}%`;
    fillAts.style.width = `${sub.ats_health}%`;

    // 3. Render Target Company Intelligence & Acceptance Roadmap
    renderCompanyRoadmap(data.company_profile, data.company_roadmap);

    // 4. Skills Match
    const skills = data.skills_analysis;
    matchedSkillsCount.textContent = skills.matched_skills.length;
    missingSkillsCount.textContent = skills.missing_skills.length;

    matchedSkillsTags.innerHTML = skills.matched_skills.length > 0
      ? skills.matched_skills.map((s) => `<span class="skill-chip chip-matched">✓ ${escapeHtml(s)}</span>`).join("")
      : `<span style="font-size: 0.8rem; color: var(--text-muted);">No exact target skills matched yet</span>`;

    missingSkillsTags.innerHTML = skills.missing_skills.length > 0
      ? skills.missing_skills.map((s) => `<span class="skill-chip chip-missing" title="Click to copy suggested skill">+ ${escapeHtml(s)}</span>`).join("")
      : `<span style="font-size: 0.8rem; color: var(--color-success);">All required skills are present in resume!</span>`;

    missingSkillsTags.querySelectorAll(".chip-missing").forEach((chip) => {
      chip.style.cursor = "pointer";
      chip.addEventListener("click", () => {
        const skillName = chip.textContent.replace("+ ", "").trim();
        navigator.clipboard.writeText(skillName);
        chip.textContent = "Copied!";
        setTimeout(() => (chip.textContent = "+ " + skillName), 1200);
      });
    });

    renderCategoryTable(skills.categories);

    // 5. Improvement Tips
    renderImprovementTips(data.improvement_tips);

    // 6. Suggested Bullets
    renderSuggestedBullets(data.suggested_bullet_points);

    // 7. Requirements Matrix
    renderRequirementsTable(data.requirements_analysis);

    // 8. ATS Diagnostics
    renderATSDiagnostics(data.ats_analysis);
  }

  function animateScoreGauge(score) {
    const circumference = 2 * Math.PI * 68;
    const offset = circumference - (score / 100) * circumference;

    gaugeProgress.style.strokeDashoffset = offset;
    if (score >= 80) gaugeProgress.style.stroke = "#10b981";
    else if (score >= 65) gaugeProgress.style.stroke = "#3b82f6";
    else if (score >= 50) gaugeProgress.style.stroke = "#f59e0b";
    else gaugeProgress.style.stroke = "#ef4444";

    let current = 0;
    const stepTime = Math.max(10, Math.floor(1000 / (score || 1)));
    const timer = setInterval(() => {
      current += 1;
      resOverallScore.textContent = current;
      if (current >= score) {
        clearInterval(timer);
        resOverallScore.textContent = score;
      }
    }, stepTime);
  }

  function applyGradeStyle(grade, elem) {
    if (grade.startsWith("A")) {
      elem.style.background = "var(--color-success-bg)";
      elem.style.borderColor = "var(--color-success-border)";
      elem.style.color = "#34d399";
    } else if (grade.startsWith("B")) {
      elem.style.background = "var(--color-blue-bg)";
      elem.style.borderColor = "rgba(59, 130, 246, 0.3)";
      elem.style.color = "#60a5fa";
    } else if (grade.startsWith("C")) {
      elem.style.background = "var(--color-warning-bg)";
      elem.style.borderColor = "var(--color-warning-border)";
      elem.style.color = "#fbbf24";
    } else {
      elem.style.background = "var(--color-danger-bg)";
      elem.style.borderColor = "var(--color-danger-border)";
      elem.style.color = "#f87171";
    }
  }

  // 9. Render Company Roadmap & Intelligence
  function renderCompanyRoadmap(profile, roadmap) {
    if (!profile || !roadmap) {
      document.getElementById("companyRoadmapSection").classList.add("hidden");
      return;
    }
    document.getElementById("companyRoadmapSection").classList.remove("hidden");

    roadmapCompanyTitle.textContent = `${profile.company_name} Hiring Intel & Acceptance Roadmap`;
    roadmapStatusBadge.textContent = roadmap.eligibility_status;

    if (roadmap.eligibility_status === "Eligible") {
      roadmapStatusBadge.className = "eligibility-status-badge status-eligible";
    } else if (roadmap.eligibility_status === "Conditionally Eligible") {
      roadmapStatusBadge.className = "eligibility-status-badge status-conditional";
    } else {
      roadmapStatusBadge.className = "eligibility-status-badge status-action-required";
    }

    // Eligibility Column
    roadmapEligibilityList.innerHTML = roadmap.eligibility_details
      .map((d) => `<div class="intel-bullet"><span>${escapeHtml(d)}</span></div>`)
      .join("");

    // Expectations Column
    const dsaInfo = profile.coding_expectations;
    const projInfo = profile.project_expectations || [];
    roadmapExpectationsList.innerHTML = `
      <div class="intel-bullet"><strong>Coding Difficulty:</strong> ${escapeHtml(dsaInfo.dsa_difficulty || "Medium")}</div>
      <div class="intel-bullet"><strong>Key DSA Focus:</strong> ${escapeHtml((dsaInfo.primary_topics || []).slice(0, 4).join(", "))}</div>
      <div class="intel-bullet"><strong>Project Benchmark:</strong> ${escapeHtml(projInfo[0] || "Production-grade project")}</div>
    `;

    // Gaps Column
    if (roadmap.resume_gaps_for_company.length > 0) {
      roadmapGapsList.innerHTML = roadmap.resume_gaps_for_company
        .map((g) => `<div class="intel-bullet" style="color: #fca5a5;"><span>${escapeHtml(g)}</span></div>`)
        .join("");
    } else {
      roadmapGapsList.innerHTML = `<div class="intel-bullet" style="color: #34d399;"><span>Your resume satisfies all primary criteria for ${profile.company_name}!</span></div>`;
    }

    // Exam Rounds Timeline
    examRoundsList.innerHTML = profile.exam_pattern
      .map((rnd) => `
        <div class="exam-round-item">
          <div class="round-header">
            <span class="round-badge">Round ${rnd.round_number}</span>
            <span class="round-duration">${escapeHtml(rnd.duration)}</span>
          </div>
          <h5 class="round-name">${escapeHtml(rnd.name)}</h5>
          <p class="round-desc">${escapeHtml(rnd.description)}</p>
          <div class="round-tags">
            ${(rnd.focus_areas || []).map((fa) => `<span class="round-tag">${escapeHtml(fa)}</span>`).join("")}
          </div>
        </div>
      `)
      .join("");

    // Must-Have Additions List
    mustHaveList.innerHTML = roadmap.must_have_additions
      .map((m) => `<div class="must-have-item">${escapeHtml(m)}</div>`)
      .join("");
  }

  function renderCategoryTable(categories) {
    const catKeys = Object.keys(categories);
    if (catKeys.length === 0) {
      categoryTableBody.innerHTML = `<p style="font-size:0.8rem; color:var(--text-muted);">No categorical skills found.</p>`;
      return;
    }

    categoryTableBody.innerHTML = catKeys
      .map((cat) => {
        const c = categories[cat];
        const matched = c.matched || [];
        const missing = c.missing || [];
        const total = matched.length + missing.length;
        const percent = total > 0 ? Math.round((matched.length / total) * 100) : 0;

        return `
        <div class="cat-row">
          <span class="cat-name">${escapeHtml(cat)}</span>
          <div class="cat-details">
            <span class="cat-stat" style="color: #34d399;">${matched.length} Matched</span>
            <span class="cat-stat" style="color: #fca5a5;">${missing.length} Missing</span>
            <span class="cat-stat" style="font-weight: 700; color: var(--text-primary); font-family: var(--font-mono);">${percent}%</span>
          </div>
        </div>
      `;
      })
      .join("");
  }

  function renderImprovementTips(tips) {
    if (!tips || tips.length === 0) {
      improvementTipsList.innerHTML = `<p style="font-size:0.85rem; color:var(--color-success);">Great job! No major critical issues were identified.</p>`;
      return;
    }

    improvementTipsList.innerHTML = tips
      .map((t) => {
        const priorityClass = `priority-${t.priority}`;
        const badgeClass = `tip-badge-${t.priority}`;
        return `
        <div class="tip-card ${priorityClass}">
          <div class="tip-header">
            <h4 class="tip-title">${escapeHtml(t.title)}</h4>
            <span class="tip-badge ${badgeClass}">${t.priority.toUpperCase()} PRIORITY</span>
          </div>
          <p class="tip-desc">${escapeHtml(t.description)}</p>
          ${
            t.action_item
              ? `<div class="tip-action-box"><strong>Recommended Action:</strong> ${escapeHtml(t.action_item)}</div>`
              : ""
          }
        </div>
      `;
      })
      .join("");
  }

  function renderSuggestedBullets(bullets) {
    if (!bullets || bullets.length === 0) {
      suggestedBulletsList.innerHTML = `<p style="font-size:0.8rem; color:var(--text-muted);">No suggested bullets generated.</p>`;
      return;
    }

    suggestedBulletsList.innerHTML = bullets
      .map((b) => `
        <div class="bullet-item">
          <span>• ${escapeHtml(b)}</span>
          <button class="btn-copy" onclick="copyBullet(this, '${escapeHtmlForAttr(b)}')">Copy</button>
        </div>
      `)
      .join("");
  }

  window.copyBullet = function (btn, text) {
    navigator.clipboard.writeText(text);
    const original = btn.textContent;
    btn.textContent = "Copied!";
    setTimeout(() => (btn.textContent = original), 1500);
  };

  function renderRequirementsTable(reqs) {
    if (!reqs || reqs.length === 0) {
      requirementsTableBody.innerHTML = `<tr><td colspan="3" style="text-align: center; color: var(--text-muted);">No distinct job requirements extracted.</td></tr>`;
      return;
    }

    requirementsTableBody.innerHTML = reqs
      .map((r) => {
        let badgeClass = "status-weak";
        if (r.status === "Strong Match") badgeClass = "status-strong";
        else if (r.status === "Moderate Match") badgeClass = "status-moderate";

        return `
        <tr>
          <td><strong style="color: var(--text-primary);">${escapeHtml(r.requirement)}</strong></td>
          <td style="color: var(--text-secondary); font-style: italic;">
            "${escapeHtml(r.best_matching_resume_text || "No direct evidence found")}"
          </td>
          <td style="text-align: center;">
            <span class="status-badge ${badgeClass}">${r.similarity}% ${r.status}</span>
          </td>
        </tr>
      `;
      })
      .join("");
  }

  function renderATSDiagnostics(ats) {
    const allSections = ["Summary / Objective", "Experience", "Education", "Skills", "Projects", "Certifications"];
    atsSectionsList.innerHTML = allSections
      .map((sec) => {
        const found = ats.sections_found.includes(sec);
        return `
        <div class="check-item ${found ? "check-pass" : "check-fail"}">
          <span>${found ? "✓" : "✗"}</span>
          <span>${sec}</span>
        </div>
      `;
      })
      .join("");

    atsMetricsList.innerHTML = ats.metrics_found.length > 0
      ? ats.metrics_found.map((m) => `<span class="metric-pill">${escapeHtml(m)}</span>`).join("")
      : `<span style="font-size:0.75rem; color:var(--text-muted);">No numbers/percentages found</span>`;

    atsVerbsList.innerHTML = ats.action_verbs_found.length > 0
      ? ats.action_verbs_found.map((v) => `<span class="verb-pill">${escapeHtml(v)}</span>`).join("")
      : `<span style="font-size:0.75rem; color:var(--text-muted);">No strong action verbs</span>`;

    const contact = ats.contact_info;
    atsContactList.innerHTML = `
      <div class="check-item ${contact.has_email ? "check-pass" : "check-fail"}">
        <span>${contact.has_email ? "✓" : "✗"}</span>
        <span>Email Address</span>
      </div>
      <div class="check-item ${contact.has_phone ? "check-pass" : "check-fail"}">
        <span>${contact.has_phone ? "✓" : "✗"}</span>
        <span>Phone Number</span>
      </div>
      <div class="check-item ${contact.has_linkedin_github ? "check-pass" : "check-fail"}">
        <span>${contact.has_linkedin_github ? "✓" : "✗"}</span>
        <span>LinkedIn / GitHub URL</span>
      </div>
      <div class="check-item" style="color: var(--text-muted); margin-top: 0.25rem;">
        <span>📄</span>
        <span>${ats.word_count.toLocaleString()} Words (~${ats.estimated_pages} page)</span>
      </div>
    `;
  }

  // 10. Export & Print
  btnExportJson.addEventListener("click", () => {
    if (!latestScoreResult) return;
    const blob = new Blob([JSON.stringify(latestScoreResult, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `resume-score-${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  });

  btnPrintReport.addEventListener("click", () => {
    window.print();
  });

  // Utilities
  function escapeHtml(str) {
    if (!str) return "";
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function escapeHtmlForAttr(str) {
    if (!str) return "";
    return str.replace(/'/g, "\\'").replace(/"/g, "&quot;");
  }
});
