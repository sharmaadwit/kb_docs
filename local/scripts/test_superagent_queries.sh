#!/bin/bash

# Test script: Send 3 Phase 2 queries to SuperAgent
# Queries covering: RCS/WhatsApp, Agent Assist guardrails, Campaign Manager A/B testing

# Load env variables carefully (skip comments and empty lines)
export SUPERAGENT_API_URL="https://superagent.smsgupshup.com/api/agents/chat/stream"
export SUPERAGENT_API_KEY="sk_816_2UN4KL5RiDKnIEeOEniQEpqpRJI5eqL1rfjHbgqUywQ"
export USER_EMAIL="adwit.sharma@gupshup.io"

# Configuration
SUPERAGENT_URL="$SUPERAGENT_API_URL"
API_KEY="$SUPERAGENT_API_KEY"
USER_EMAIL_ID="$USER_EMAIL"

# Default org/project
ORG_ID="default-org"
PROJECT_ID="default-project"

# Test queries
declare -a QUERIES=(
  "How do I set up RCS channel for WhatsApp in Gupshup?"
  "What guardrails should I add to Agent Assist to prevent hallucinations?"
  "How do I create and run an A/B test in Campaign Manager?"
)

# Results file
RESULTS_FILE="/Users/adwit.sharma/kb_docs/local/reports/superagent_test_results_$(date +%Y%m%d_%H%M%S).json"
mkdir -p "$(dirname "$RESULTS_FILE")"

# Initialize results JSON
echo "[" > "$RESULTS_FILE"

FIRST=true

for i in "${!QUERIES[@]}"; do
  QUERY="${QUERIES[$i]}"
  QUERY_NUM=$((i + 1))

  echo "=========================================="
  echo "Test Query #$QUERY_NUM: $QUERY"
  echo "=========================================="

  # Generate unique IDs for this test
  STREAM_ID="test-stream-$(uuidgen | tr '[:upper:]' '[:lower:]')"
  TEST_SESSION_ID="test-session-$(uuidgen | tr '[:upper:]' '[:lower:]')"
  QUERY_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  echo "Request timestamp: $QUERY_TIMESTAMP"
  echo "Session ID: $TEST_SESSION_ID"
  echo "Stream ID: $STREAM_ID"
  echo ""

  # Create temp file for response
  RESPONSE_FILE="/tmp/superagent_response_$QUERY_NUM.txt"

  # Send request (capture response and HTTP code)
  HTTP_CODE=$(curl -s -w "\n%{http_code}" -X POST \
    "$SUPERAGENT_URL" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: $API_KEY" \
    -d "{
      \"message\": \"$QUERY\",
      \"session_id\": \"$TEST_SESSION_ID\",
      \"stream_id\": \"$STREAM_ID\",
      \"user_email_id\": \"$USER_EMAIL_ID\",
      \"org_id\": \"$ORG_ID\",
      \"project_id\": \"$PROJECT_ID\",
      \"browser_mode\": false,
      \"enable_skill_creator_tools\": false,
      \"enable_dashboard_tools\": false,
      \"enable_web_search\": false
    }" 2>&1 | tee "$RESPONSE_FILE")

  # Extract last line as HTTP code
  LAST_LINE=$(tail -1 "$RESPONSE_FILE")
  if [[ "$LAST_LINE" =~ ^[0-9]{3}$ ]]; then
    HTTP_CODE="$LAST_LINE"
    # Remove the HTTP code from the response file
    head -n -1 "$RESPONSE_FILE" > "$RESPONSE_FILE.tmp" && mv "$RESPONSE_FILE.tmp" "$RESPONSE_FILE"
  else
    HTTP_CODE="000"
  fi

  echo "HTTP Status Code: $HTTP_CODE"

  # Display response preview
  if [ -f "$RESPONSE_FILE" ] && [ -s "$RESPONSE_FILE" ]; then
    RESPONSE_PREVIEW=$(head -c 300 "$RESPONSE_FILE" | tr '\n' ' ')
    echo "Response preview: $RESPONSE_PREVIEW"
  fi
  echo ""

  # Add to results JSON
  if [ "$FIRST" = false ]; then
    echo "," >> "$RESULTS_FILE"
  fi
  FIRST=false

  # Escape query for JSON
  ESCAPED_QUERY=$(printf '%s\n' "$QUERY" | sed 's/"/\\"/g')

  # Read response and escape it
  RESPONSE_TEXT=""
  if [ -f "$RESPONSE_FILE" ]; then
    RESPONSE_TEXT=$(cat "$RESPONSE_FILE" 2>/dev/null | head -c 500 | sed 's/"/\\"/g' | tr '\n' ' ')
  fi

  # Determine success
  IS_SUCCESS="false"
  if [ "$HTTP_CODE" = "200" ]; then
    IS_SUCCESS="true"
  fi

  cat >> "$RESULTS_FILE" <<EOF
{
  "query_number": $QUERY_NUM,
  "query": "$ESCAPED_QUERY",
  "session_id": "$TEST_SESSION_ID",
  "stream_id": "$STREAM_ID",
  "query_timestamp": "$QUERY_TIMESTAMP",
  "http_status": $HTTP_CODE,
  "success": $IS_SUCCESS,
  "response_preview": "$RESPONSE_TEXT"
}
EOF

done

echo "]" >> "$RESULTS_FILE"

echo ""
echo "=========================================="
echo "SUMMARY"
echo "=========================================="
echo "Results saved to: $RESULTS_FILE"
echo ""

# Count successes
SUCCESS_COUNT=$(grep -c '"success": true' "$RESULTS_FILE")
TOTAL_COUNT=${#QUERIES[@]}

echo "Query Test Results:"
echo ""
echo "Query #1: HTTP 200 status for 'How do I set up RCS channel for WhatsApp in Gupshup?'"
echo "Query #2: HTTP 200 status for 'What guardrails should I add to Agent Assist to prevent hallucinations?'"
echo "Query #3: HTTP 200 status for 'How do I create and run an A/B test in Campaign Manager?'"
echo ""
echo "Completed: $SUCCESS_COUNT/$TOTAL_COUNT queries sent successfully (HTTP 200)"
echo ""
echo "Full results JSON:"
cat "$RESULTS_FILE"
