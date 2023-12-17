def user_prompt(prompt):
    return [{"role": "user", "content": prompt}]

def system_prompt(prompt):
    return [{"role": "system", "content": prompt}]

def request_detailed_result():
    return system_prompt("Don't make assumptions about what values to plug into functions. Stop the conversation If a user request is ambiguous.") + \
        system_prompt("Be detailed with how you calculate a result")

def summarize():
    return system_prompt("Do not respond to the user, summarize the assistant, ideally one sentence, fewer than 12 words, use the third person, and do not use the word 'I'")
def remain_functional():
    return system_prompt("If the user ask things outside of the functions provided, you can say something like: I don't understand")
