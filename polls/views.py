#!/usr/bin/python
# -*- coding: utf-8 -*-

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from polls.models import Poll, Choice
from django.template import Context, loader, RequestContext
from django.core.mail import send_mail


def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]

    # Can either do this
    # t = loader.get_template('index.html')
    # c = Context({'latest_poll_list': latest_poll_list})
    # return HttpResponse(t.render(c))
    # Or use this shortcut below

    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render_to_response('index.html',
                              {'latest_poll_list': latest_poll_list})


def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('detail.html', {'poll': p},
                              context_instance=RequestContext(request))


def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('results.html', {'poll': p})


def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):

        # Redisplay the poll voting form.

        return render_to_response('detail.html', {'poll': p,
                                  'error_message': "You didn't select a choice."
                                                  },
                                  context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.

        # email

        # send_mail('Subject here', 'Here is the message.',
        #           'from@example.com', ['mohit.kanwal@gmail.com'],
        #           fail_silently=False)

        
        return HttpResponseRedirect(reverse('poll_results', args=(p.id,
                                                                  )))


def mail(sender, receiver, Message):
    import smtplib
    print "Sending email"
    try:
        s = smtplib.SMTP("smtp.nus.edu.sg")
        s.ehlo()
        s.set_debuglevel(1)
        s.starttls()
        s.ehlo()
        # s.connect()
        msg = ("From: %s\r\nTo: %s\r\n\r\n"
               % (sender, receiver))
        Message = msg + "\n" + Message
        #s.login("<>", "<>")
        s.sendmail(sender, receiver, Message)
    except Exception, R:
            print R
            return R