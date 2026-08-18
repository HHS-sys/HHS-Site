const assert = require("node:assert/strict");
const quoteHandler = require("../api/quote.js");

const VALID_ID = "f47ac10b-58cc-4372-a567-0e02b2c3d479";

function request(overrides = {}) {
  const body = {
    submissionId: VALID_ID,
    name: "Website Test",
    location: "London, Ontario",
    phone: "519-555-0100",
    email: "customer@example.com",
    service: "Bathroom Renovations",
    timing: "Flexible",
    message: "We would like to discuss a bathroom renovation.",
    website: "",
    ...(overrides.body || {}),
  };
  return {
    method: "POST",
    headers: {
      host: "www.hekmanhomeservices.ca",
      origin: "https://www.hekmanhomeservices.ca",
      accept: "application/json",
      "content-type": "application/json",
      "content-length": String(Buffer.byteLength(JSON.stringify(body))),
      ...(overrides.headers || {}),
    },
    body,
    ...Object.fromEntries(
      Object.entries(overrides).filter(([key]) => key !== "body" && key !== "headers"),
    ),
  };
}

function response() {
  return {
    headers: {},
    statusCode: 0,
    payload: null,
    setHeader(name, value) {
      this.headers[name.toLowerCase()] = value;
    },
    end(value) {
      this.raw = value || "";
      this.payload = value ? JSON.parse(value) : null;
    },
  };
}

async function run(input) {
  const output = response();
  await quoteHandler(input, output);
  return output;
}

async function main() {
  const originalFetch = global.fetch;
  const originalKey = process.env.RESEND_API_KEY;
  const originalLog = console.log;
  const originalError = console.error;
  const calls = [];

  console.log = () => {};
  console.error = () => {};
  process.env.RESEND_API_KEY = "re_test_only";
  global.fetch = async (url, options) => {
    calls.push({ url, options });
    return {
      ok: true,
      status: 200,
      async json() {
        return { id: "email_test" };
      },
    };
  };

  try {
    const sent = await run(request());
    assert.equal(sent.statusCode, 200);
    assert.deepEqual(sent.payload, { ok: true });
    assert.equal(calls.length, 1);
    assert.equal(calls[0].url, "https://api.resend.com/emails");
    assert.equal(
      calls[0].options.headers["Idempotency-Key"],
      `website-quote-${VALID_ID}`,
    );
    const sentPayload = JSON.parse(calls[0].options.body);
    assert.deepEqual(sentPayload.to, ["hekmanhomeservices@gmail.com"]);
    assert.equal(sentPayload.reply_to, "customer@example.com");
    assert.equal(sentPayload.from, "Hekman Home Services <quotes@hekmanhomeservices.ca>");

    calls.length = 0;
    const phoneOnly = await run(request({ body: { email: "" } }));
    assert.equal(phoneOnly.statusCode, 200);
    assert.equal("reply_to" in JSON.parse(calls[0].options.body), false);

    calls.length = 0;
    const trapped = await run(request({ body: { website: "spam.example" } }));
    assert.equal(trapped.statusCode, 200);
    assert.equal(calls.length, 0);

    const nativeFields = new URLSearchParams({
      name: "Native Form Test",
      location: "London, Ontario",
      phone: "519-555-0100",
      email: "",
      service: "Handyman Work & Home Repairs",
      timing: "Flexible",
      message: "Please contact us about a group of home repairs.",
      website: "",
    }).toString();
    const nativeResult = await run({
      method: "POST",
      headers: {
        host: "www.hekmanhomeservices.ca",
        origin: "https://www.hekmanhomeservices.ca",
        accept: "text/html",
        "content-type": "application/x-www-form-urlencoded",
        "content-length": String(Buffer.byteLength(nativeFields)),
      },
      body: nativeFields,
    });
    assert.equal(nativeResult.statusCode, 303);
    assert.equal(nativeResult.headers.location, "/contact/?quote=sent#quote-sent");

    const missingContact = await run(
      request({ body: { phone: "", email: "" } }),
    );
    assert.equal(missingContact.statusCode, 400);

    const badOrigin = await run(
      request({ headers: { origin: "https://example.com" } }),
    );
    assert.equal(badOrigin.statusCode, 403);

    const missingOrigin = await run(
      request({ headers: { origin: undefined } }),
    );
    assert.equal(missingOrigin.statusCode, 403);

    const wrongMethod = await run(request({ method: "GET" }));
    assert.equal(wrongMethod.statusCode, 405);
    assert.equal(wrongMethod.headers.allow, "POST");

    const wrongContentType = await run(
      request({ headers: { "content-type": "text/plain" } }),
    );
    assert.equal(wrongContentType.statusCode, 415);

    const malformedJson = await run({
      method: "POST",
      headers: {
        host: "www.hekmanhomeservices.ca",
        origin: "https://www.hekmanhomeservices.ca",
        accept: "application/json",
        "content-type": "application/json",
        "content-length": "1",
      },
      body: "{",
    });
    assert.equal(malformedJson.statusCode, 400);

    const oversized = await run(
      request({ headers: { "content-length": "20001" } }),
    );
    assert.equal(oversized.statusCode, 413);

    const unexpectedField = await run(
      request({ body: { marketingOptIn: "yes" } }),
    );
    assert.equal(unexpectedField.statusCode, 400);

    const escaped = quoteHandler._private.emailContent({
      name: "<Steph & Rene>",
      phone: "519-555-0100",
      email: "customer@example.com",
      location: "London",
      service: "",
      timing: "",
      message: "Please fix <this> & that.",
    });
    assert.match(escaped.html, /&lt;Steph &amp; Rene&gt;/);
    assert.match(escaped.html, /&lt;this&gt; &amp; that/);
    assert.doesNotMatch(escaped.html, /<Steph/);

    delete process.env.RESEND_API_KEY;
    const unconfigured = await run(request());
    assert.equal(unconfigured.statusCode, 503);

    process.env.RESEND_API_KEY = "re_test_only";
    global.fetch = async () => ({ ok: false, status: 422 });
    const providerFailure = await run(request());
    assert.equal(providerFailure.statusCode, 502);
    assert.match(providerFailure.payload.error, /could not send/i);
  } finally {
    global.fetch = originalFetch;
    console.log = originalLog;
    console.error = originalError;
    if (originalKey === undefined) delete process.env.RESEND_API_KEY;
    else process.env.RESEND_API_KEY = originalKey;
  }

  console.log("Quote API tests passed.");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
