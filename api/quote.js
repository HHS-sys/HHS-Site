const { randomUUID } = require("node:crypto");

const ALLOWED_SERVICES = new Set([
  "",
  "Bathroom Renovations",
  "Drywall & Ceiling Repair",
  "Kitchen Renovations",
  "Flooring Installation",
  "Basement Renovations",
  "Handyman Work & Home Repairs",
  "Decks & Exterior Work",
  "Restoration & Damage Repairs",
  "Commercial Maintenance & Repairs",
  "Structural & Layout Changes",
  "Popcorn Ceiling Removal",
  "Multiple services / other",
]);

const MAX_BODY_BYTES = 20_000;
const RATE_LIMIT_WINDOW_MS = 10 * 60 * 1000;
const RATE_LIMIT_MAX = 5;
const RATE_BUCKETS_MAX = 5_000;
const rateBuckets = new Map();
const UUID_PATTERN =
  /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function header(request, name) {
  const value = request.headers?.[name] ?? request.headers?.[name.toLowerCase()];
  return Array.isArray(value) ? value[0] : value;
}

function sendJson(response, status, payload) {
  response.statusCode = status;
  response.setHeader("Content-Type", "application/json; charset=utf-8");
  response.setHeader("Cache-Control", "no-store");
  response.end(JSON.stringify(payload));
}

function parseRequestBody(request) {
  const contentType = String(header(request, "content-type") || "")
    .split(";", 1)[0]
    .trim()
    .toLowerCase();
  if (
    contentType !== "application/json" &&
    contentType !== "application/x-www-form-urlencoded"
  ) {
    const error = new Error("Unsupported content type");
    error.status = 415;
    error.reason = "unsupported_content_type";
    throw error;
  }

  const contentLength = Number(header(request, "content-length") || 0);
  if (Number.isFinite(contentLength) && contentLength > MAX_BODY_BYTES) {
    const error = new Error("Request is too large");
    error.status = 413;
    error.reason = "request_too_large";
    throw error;
  }

  let body = request.body;
  if (Buffer.isBuffer(body)) body = body.toString("utf8");
  if (typeof body === "string") {
    if (Buffer.byteLength(body, "utf8") > MAX_BODY_BYTES) {
      const error = new Error("Request is too large");
      error.status = 413;
      error.reason = "request_too_large";
      throw error;
    }
    if (contentType === "application/json") {
      try {
        body = JSON.parse(body);
      } catch {
        const error = new Error("Invalid JSON");
        error.status = 400;
        error.reason = "invalid_json";
        throw error;
      }
    } else {
      body = Object.fromEntries(new URLSearchParams(body));
    }
  }

  if (!body || typeof body !== "object" || Array.isArray(body)) {
    const error = new Error("Invalid request body");
    error.status = 400;
    error.reason = "invalid_request_body";
    throw error;
  }
  if (Buffer.byteLength(JSON.stringify(body), "utf8") > MAX_BODY_BYTES) {
    const error = new Error("Request is too large");
    error.status = 413;
    error.reason = "request_too_large";
    throw error;
  }
  return body;
}

function wantsJson(request) {
  return String(header(request, "accept") || "")
    .toLowerCase()
    .includes("application/json");
}

function redirectToContact(response, state) {
  response.statusCode = 303;
  response.setHeader("Cache-Control", "no-store");
  response.setHeader("Location", `/contact/?quote=${state}#quote-${state}`);
  response.end();
}

function isAllowedOrigin(request) {
  const origin = header(request, "origin");
  if (!origin) return false;

  const host = String(header(request, "host") || "").toLowerCase();
  try {
    return new URL(origin).host.toLowerCase() === host;
  } catch {
    return false;
  }
}

function clientIp(request) {
  const forwarded = String(header(request, "x-forwarded-for") || "")
    .split(",", 1)[0]
    .trim();
  const direct = String(header(request, "x-real-ip") || "").trim();
  return (forwarded || direct).slice(0, 64);
}

function enforceRateLimit(request, now = Date.now()) {
  const ip = clientIp(request);
  if (!ip) return;

  for (const [key, bucket] of rateBuckets) {
    if (now - bucket.startedAt >= RATE_LIMIT_WINDOW_MS) rateBuckets.delete(key);
  }
  if (rateBuckets.size >= RATE_BUCKETS_MAX && !rateBuckets.has(ip)) {
    rateBuckets.delete(rateBuckets.keys().next().value);
  }

  const current = rateBuckets.get(ip);
  const bucket =
    !current || now - current.startedAt >= RATE_LIMIT_WINDOW_MS
      ? { startedAt: now, count: 0 }
      : current;
  bucket.count += 1;
  rateBuckets.set(ip, bucket);

  if (bucket.count > RATE_LIMIT_MAX) {
    const error = new Error(
      "Too many enquiries were sent from this connection. Please wait a few minutes or contact us directly.",
    );
    error.status = 429;
    error.retryAfter = Math.max(
      1,
      Math.ceil((RATE_LIMIT_WINDOW_MS - (now - bucket.startedAt)) / 1000),
    );
    error.reason = "rate_limited";
    throw error;
  }
}

function value(body, key) {
  const field = body[key];
  if (field === undefined || field === null) return "";
  if (typeof field !== "string") {
    const error = new Error(`Invalid ${key}`);
    error.status = 400;
    error.reason = "invalid_field_type";
    error.invalidFields = [key];
    throw error;
  }
  return field.trim();
}

function singleLine(text) {
  return text.replace(/[\u0000-\u001f\u007f]+/g, " ").replace(/\s+/g, " ").trim();
}

function multiline(text) {
  return text
    .replace(/\r\n?/g, "\n")
    .replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g, "")
    .trim();
}

function validate(body) {
  const allowedKeys = new Set([
    "submissionId",
    "name",
    "location",
    "phone",
    "email",
    "service",
    "timing",
    "message",
    "website",
  ]);
  if (Object.keys(body).some((key) => !allowedKeys.has(key))) {
    const error = new Error("Unexpected field");
    error.status = 400;
    error.reason = "unexpected_field";
    throw error;
  }

  const fields = {
    submissionId: singleLine(value(body, "submissionId")),
    name: singleLine(value(body, "name")),
    location: singleLine(value(body, "location")),
    phone: singleLine(value(body, "phone")),
    email: singleLine(value(body, "email")).toLowerCase(),
    service: singleLine(value(body, "service")),
    timing: singleLine(value(body, "timing")),
    message: multiline(value(body, "message")),
    website: singleLine(value(body, "website")),
  };

  const invalidFields = [];
  if (!UUID_PATTERN.test(fields.submissionId)) invalidFields.push("submissionId");
  if (fields.name.length < 2 || fields.name.length > 100) invalidFields.push("name");
  if (fields.location.length < 2 || fields.location.length > 160) {
    invalidFields.push("location");
  }
  if (
    fields.phone.length > 40 ||
    (fields.phone && fields.phone.replace(/\D/g, "").length < 7)
  ) {
    invalidFields.push("phone");
  }
  if (
    fields.email.length > 254 ||
    (fields.email && !EMAIL_PATTERN.test(fields.email))
  ) {
    invalidFields.push("email");
  }
  if (fields.timing.length > 120) invalidFields.push("timing");
  if (fields.message.length < 10 || fields.message.length > 4000) {
    invalidFields.push("message");
  }
  if (!ALLOWED_SERVICES.has(fields.service)) invalidFields.push("service");
  if (!fields.phone && !fields.email) invalidFields.push("contact");

  if (invalidFields.length) {
    const error = new Error("Please review the form fields and try again");
    error.status = 400;
    error.reason = "invalid_form_fields";
    error.invalidFields = invalidFields;
    throw error;
  }
  return fields;
}

function escapeHtml(text) {
  return text.replace(/[&<>"']/g, (character) => {
    const entities = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;",
    };
    return entities[character];
  });
}

function emailContent(fields) {
  const rows = [
    ["Name", fields.name],
    ["Phone", fields.phone || "Not provided"],
    ["Email", fields.email || "Not provided"],
    ["Project location", fields.location],
    ["Project type", fields.service || "Not selected"],
    ["Preferred timing", fields.timing || "Not provided"],
  ];
  const textRows = rows.map(([label, content]) => `${label}: ${content}`).join("\n");
  const htmlRows = rows
    .map(
      ([label, content]) =>
        `<tr><th style="padding:8px 12px 8px 0;text-align:left;vertical-align:top;color:#5f6670">${escapeHtml(label)}</th><td style="padding:8px 0;vertical-align:top">${escapeHtml(content)}</td></tr>`,
    )
    .join("");
  const messageHtml = escapeHtml(fields.message).replace(/\n/g, "<br>");

  return {
    subject: `New website project enquiry — ${fields.service || "General project"}`,
    text: `${textRows}\n\nProject details:\n${fields.message}`,
    html: `<div style="font-family:Arial,sans-serif;max-width:640px;color:#172331"><h1 style="font-size:24px">New website project enquiry</h1><table style="border-collapse:collapse;width:100%">${htmlRows}</table><h2 style="margin-top:28px;font-size:18px">Project details</h2><p style="line-height:1.6">${messageHtml}</p><p style="margin-top:28px;padding-top:18px;border-top:1px solid #d9dde2;color:#6a717b;font-size:13px">Sent securely from hekmanhomeservices.ca</p></div>`,
  };
}

async function sendWithResend(fields) {
  const apiKey = process.env.RESEND_API_KEY;
  const to = process.env.QUOTE_TO_EMAIL || "hekmanhomeservices@gmail.com";
  const from =
    process.env.QUOTE_FROM_EMAIL ||
    "Hekman Home Services <quotes@hekmanhomeservices.ca>";
  if (!apiKey) {
    const error = new Error("Email delivery is not configured");
    error.status = 503;
    throw error;
  }

  const content = emailContent(fields);
  const payload = {
    from,
    to: [to],
    subject: content.subject,
    text: content.text,
    html: content.html,
  };
  if (fields.email) payload.reply_to = fields.email;

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
        "Idempotency-Key": `website-quote-${fields.submissionId}`,
      },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });
    if (!response.ok) {
      const error = new Error("Email provider rejected the request");
      error.status = 502;
      error.providerStatus = response.status;
      throw error;
    }
    return response.json();
  } finally {
    clearTimeout(timeout);
  }
}

module.exports = async function quoteHandler(request, response) {
  const started = Date.now();
  const requestId = header(request, "x-vercel-id") || "local";

  if (request.method !== "POST") {
    response.setHeader("Allow", "POST");
    return sendJson(response, 405, { ok: false, error: "Method not allowed" });
  }
  if (!isAllowedOrigin(request)) {
    return sendJson(response, 403, { ok: false, error: "Request origin is not allowed" });
  }

  try {
    const parsedBody = parseRequestBody(request);
    const fields = validate({
      ...parsedBody,
      submissionId: parsedBody.submissionId || randomUUID(),
    });
    if (fields.website) {
      return wantsJson(request)
        ? sendJson(response, 200, { ok: true })
        : redirectToContact(response, "sent");
    }

    enforceRateLimit(request);
    await sendWithResend(fields);
    console.log(
      JSON.stringify({
        level: "info",
        message: "quote_sent",
        route: "/api/quote",
        requestId,
        durationMs: Date.now() - started,
      }),
    );
    return wantsJson(request)
      ? sendJson(response, 200, { ok: true })
      : redirectToContact(response, "sent");
  } catch (error) {
    const status = Number(error.status) || 500;
    const isServerFailure = status >= 500;
    if (status === 429) {
      response.setHeader("Retry-After", String(error.retryAfter || 600));
    }
    const logEntry = JSON.stringify({
      level: isServerFailure ? "error" : "warn",
      message: isServerFailure ? "quote_failed" : "quote_rejected",
      route: "/api/quote",
      requestId,
      status,
      reason: error.reason || (isServerFailure ? "server_failure" : "client_request_rejected"),
      invalidFields: Array.isArray(error.invalidFields)
        ? error.invalidFields
        : undefined,
      providerStatus: isServerFailure ? error.providerStatus : undefined,
      durationMs: Date.now() - started,
    });
    if (isServerFailure) console.error(logEntry);
    else console.warn(logEntry);
    const publicMessage =
      isServerFailure
        ? "We could not send your enquiry right now. Please try again or contact us directly."
        : error.message;
    return wantsJson(request)
      ? sendJson(response, status, { ok: false, error: publicMessage })
      : redirectToContact(response, "error");
  }
};

module.exports._private = {
  emailContent,
  enforceRateLimit,
  isAllowedOrigin,
  parseRequestBody,
  rateBuckets,
  validate,
};
