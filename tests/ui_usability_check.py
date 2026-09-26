"""Focused regression checks for navigation, editing and document selection."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.packages'))
from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000})
    errors=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto('http://127.0.0.1:8000')
    page.get_by_role('button',name='Explore a sample',exact=False).click()
    page.locator('#jurisdiction').select_option('Unknown')
    page.locator('#submit-upload').click()
    page.locator('.source-clause').first.wait_for()
    page.locator('#run-ai').click()
    page.get_by_role('heading',name='Know what is connected.').wait_for()
    page.goto('http://127.0.0.1:8000/#documents')
    page.locator('#document-search').fill('freelancer')
    assert page.locator('.doc-card:visible').count()==1
    page.locator('#document-search').fill('no match here')
    assert page.locator('.doc-card:visible').count()==0
    assert 'No matching' in page.locator('#document-count').inner_text()
    page.goto('http://127.0.0.1:8000/#compare')
    page.locator('.compare-row').first.wait_for()
    assert page.locator('.compare-row').count()==4
    page.goto('http://127.0.0.1:8000/#actions')
    page.locator('#action-document').select_option(index=2)
    page.locator('#generate-tasks').click()
    page.locator('[data-edit-task]').first.wait_for()
    data=page.evaluate("fetch('/api/state').then(r=>r.json())")
    freelance=next(d for d in data['documents'] if 'Freelancer' in d['name'])
    assert all(t['document_id']==freelance['id'] for t in data['tasks'])
    page.goto('http://127.0.0.1:8000/#brief')
    page.locator('#objective').fill('Clarify my freelance payment schedule')
    page.locator('#facts').fill('I have not signed yet.')
    page.locator('#brief-text').fill('My unsaved-looking edit must survive navigating away.')
    page.locator('#nav a[href="#overview"]').click()
    page.locator('#nav a[href="#brief"]').click()
    assert page.locator('#brief-text').input_value()=='My unsaved-looking edit must survive navigating away.'
    assert page.locator('#objective').input_value()=='Clarify my freelance payment schedule'
    assert page.locator('#facts').input_value()=='I have not signed yet.'
    page.locator('#brief-text').fill('This edit is automatically saved.')
    expect(page.locator('#brief-save-state')).to_have_text('Saved in this session')
    page.reload()
    assert page.locator('#brief-text').input_value()=='This edit is automatically saved.'
    page.set_viewport_size({'width':390,'height':844})
    page.locator('#menu').click()
    assert page.locator('.sidebar').evaluate('el=>!el.inert')
    assert page.locator('.body').evaluate('el=>el.inert')
    page.keyboard.press('Escape')
    assert page.locator('.sidebar').evaluate('el=>el.inert')
    assert page.locator('.body').evaluate('el=>!el.inert')
    page.locator('#menu').click()
    page.locator('#nav-backdrop').click(position={'x':350,'y':400})
    assert page.locator('#menu').get_attribute('aria-expanded')=='false'
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    assert not errors,errors
    browser.close()
print('UI usability checks passed: search, automatic comparison, selected-document checklist, brief autosave/navigation, AI setup link, and mobile keyboard/backdrop navigation.')
